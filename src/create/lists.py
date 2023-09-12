import time
from src.clients.radarr import RadarrInteractions
from datetime import datetime
import logging
import random
import json


class Lists:
    def __init__(self, config):
        self.config = config
        self.plex = config.get_client('plex')
        self.emby = config.get_client('emby')
        self.chat = config.get_client('chat')

    def sync_plex_watchlist(self):
        plex_watchlist = self.config.get_account('myplex').watchlist()

        emby_watchlist = self.emby.create_collection('Watchlist', 'Mixed')

        for media in plex_watchlist:
            print(f'Processing media: {media.title}')

            emby_type = 'Series' if (media.type == 'episode' or media.type == 'show') else 'Movie'

            emby_media_items = self.emby.search(media.title, emby_type)

            for emby_media in emby_media_items:
                try:
                    if emby_media['ProductionYear'] == media.year:
                        print(f'Adding {media.title} to Emby Watchlist {emby_media["Type"]}')
                        if emby_media['Type'] == 'Episode':
                            self.emby.add_item_to_collection(emby_watchlist['Id'], emby_media['SeriesId'])
                        else:
                            self.emby.add_item_to_collection(emby_watchlist['Id'], emby_media['Id'])
                        continue
                    else:
                        print(f'No match found in Emby for {media.title}')
                        logging.warning(f'No match found in Emby for {media.title}')
                except KeyError:
                    print(f'KEY ERROR: No match found in Emby for {media.title}')

    def create_previously_watchedlist(self):
        emby_watchlist = self.emby.get_collection_by_name('Watchlist')
        emby_previously_watchlist = self.emby.create_collection('Previously Watched', 'Mixed',
                                                                '!000_Watchlist_Previously_Watched')

        # TODO: Use new Poster logic to create poster
        # self.emby.create_poster(f'{self.config.get_config_path()}/previously-watched.png', 'Previously Watched',
        #                         self.config.get_root_path(), f'{self.config.get_root_path()}/resources/eye-closed.png')
        # self.emby.upload_image(emby_previously_watchlist['Id'],
        #                        f'{self.config.get_config_path()}/previously-watched.png')

        print('emby_watchlist', emby_watchlist)

        watchlist_items, watchlist_length = self.emby.get_items_in_collection(emby_watchlist['Id'])

        # print(watchlist_items)

        for item in watchlist_items:
            # print('item', item)
            item_id = item['Id']
            item_metadata = self.emby.get_item_metadata(item_id)

            # Check if the LastPlayedDate is greater than June of 2022
            may_2023 = datetime(2023, 5, 1).date()

            # 2023-07-02T15:02:51.0000000Z
            last_played_date_str = item_metadata.get('UserData', {}).get('LastPlayedDate',
                                                                         '1970-01-01T00:00:00.0000000Z')  # Truncate the time zone part
            last_played_date_str_truncated = last_played_date_str[:-6]  # Truncate the time zone part
            last_played_date = datetime.strptime(last_played_date_str_truncated, '%Y-%m-%dT%H:%M:%S.%f').date()

            if (last_played_date > may_2023 and item_metadata['UserData']['PlayCount'] > 0) or (
                last_played_date > may_2023 and item_metadata['UserData']['Played'] == True):
                print(f'Moving {item_metadata["Name"]} to Previously Watched')

                self.emby.add_item_to_collection(emby_previously_watchlist['Id'], item_id)
                self.emby.delete_item_from_collection(emby_watchlist['Id'], item_id)

    def create_sleeping_shows_playlist(self, name, shows, if_exists_delete=True):
        config = self.config
        root_path = config.get_root_path()
        config_path = config.get_config_path()

        logging.basicConfig(filename=f'{config_path}/logs/playlist.log', level=logging.INFO)

        emby = config.get_client('emby')

        all_media = []

        playlists = emby.get_playlists()
        print(playlists)

        if if_exists_delete:
            emby.delete_playlist(playlists[0]['Id'])

        playlist = emby.create_playlist(name, 'Series')
        # Fetch all episodes from each show
        for show_name in shows:
            print(f'Fetching episodes for {show_name}')
            show = emby.search(show_name, 'Series')[0]
            seasons = emby.get_seasons(show['Id'])

            # print(seasons)

            for season in seasons:
                episodes = emby.get_episodes(show['Id'], season['Id'])
                print(f'Fetched {len(episodes)} episodes for {show_name}')
                for episode in episodes:
                    # print(episode)
                    all_media.append(episode['Id'])

        print(f'Total number of media items: {len(all_media)}')

        # Shuffle all the media items
        random.shuffle(all_media)
        # Create a new playlist with the first 500 media items, or all items if there are less than 500
        playlist_items = all_media[:3000] if len(all_media) > 3000 else all_media
        # plex.createPlaylist('Sleeping Shows', 'TV Shows', playlist_items)

        print(all_media)

        for item in playlist_items:
            emby.add_item_to_playlist(playlist['Id'], item)

        PosterImageCreator.create_emby_poster(f'{config_path}/resources/sleeping.png', 'Sleeping Shows')

        # emby.upload_image(emby_watchlist['Id'], 'watchlist.png')

        emby.upload_image(playlist['Id'], f'{config_path}/resources/sleeping.png')

    def _get_chat_res_as_json(self, rules, movies=None, retry_count=0):
        if (retry_count > 3):
            print("Failed to get chat as json.")
            return None

        if movies is None:
            movie_content = f'Suggest movies to watch. Following the rules: {rules}'
        else:
            movie_content = f"Based on this list of movies: {movies}. Suggest more movies to watch."


        print('rules', rules)
        print('movie_content', movie_content)


        completion = self.chat.ChatCompletion.create(model="gpt-3.5-turbo",
                                                     messages=[
                                                         {"role": "system",
                                                          "content": f"I will ALWAYS respond with a json object and no text oustide of that object. \n {rules}"},
                                                         {"role": "user", "content": movie_content}
                                                     ])
        response = completion.choices[0].message.content

        print(response)

        try:
            return json.loads(response)
        except Exception as e:
            print(f"Message not in json format. Retrying... {retry_count} of 3")
            # try again...
            time.sleep(20)  # max 3 req per min
            return self._convert_res_to_json(response, rules, retry_count + 1)

    def _convert_media_list_to_names_as_csv(self, media_list):
        names = ''
        for media in media_list:
            try:
                names += media['Name'] + ', '
            except:
                names += media['name'] + ', '
        return names

    def _convert_res_to_json(self, response, rules, retry_count=0):
        if (retry_count > 2):
            print("Failed to get chat as json.")
            return None

        try:
            completion = self.chat.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": f"I will ALWAYS respond with a json object and no text outside of that object. \n {rules}"},
                    {"role": "user", "content": f"Convert this list to a json object: {response} \n {rules} "}

                ])

            print(completion.choices[0].message.content)

            return json.loads(completion.choices[0].message.content)
        except:
            print(f"Message still not in json format. ")
            # try again...

    def _process_rules(self, rules):

        for rule in rules:
            print(rule)

        return rules

    def create_collection(self, config):
        print("Creating collection:", config)

        limit = config['options']['limit'] if 'limit' in config else 30
        media_type = config['options']['media_type'] if 'media_type' in config else None
        rules = config['rules']

        self._process_rules(rules)

        # if(config['provider'] == 'ai'):
        # self.create_emby_ai_recommended(config['name'],)

    def create_emby_ai_recommended(self, name, media_list=None, count=30, media_type="Movie", optional_rules=None,
                                   retry_count=0):
        if (retry_count > 2):
            print("Failed to completely fill the collection.")
            return None

        format_str = f'{{"{media_type}s": [{{"name": "{media_type} Name", "year": "{media_type} Year"}}]}}'
        rules = f'Return a json object with the format {format_str}.' \
                f'Provide a list of {count} movies that I have not seen. ' \
                f'Only recommend {media_type}.'

        if (retry_count > 0):
            print("Retrying AI Recommend...")
            # get movies from a collection and append to rules
            try:
                items = self.emby.get_collection_by_name(name, media_type)
                media_names = self._convert_media_list_to_names_as_csv(items)
                rules += f'Do not include these {media_type}\'s: {media_names}'
                print('Ignore:', media_names)
            except:
                print("Failed to get media list from collection, ok skipping...")

        if optional_rules is not None:
            rules += optional_rules

        if media_list is not None:
            random.shuffle(
                media_list)  # Shuffle the list so we get a random selection of movies, as we cant send all to the AI, too big possibly
            media_names = self._convert_media_list_to_names_as_csv(media_list[:400])
        else:
            media_names = ''

        json_data = self._get_chat_res_as_json(rules, media_names)

        # create a new collection
        emby_collection = self.emby.create_collection(name, media_type, f'!001__{name}')

        config_path = self.config.get_root_path()
        root_dir = self.config.get_root_path()
        icon_path = f'{config_path}/resources/ai.png'

        self.emby.create_poster(f'{config_path}/watchlist.png', name, root_dir, icon_path)
        self.emby.upload_image(emby_collection['Id'], f'{config_path}/watchlist.png')

        exclude_media = []

        for media in json_data[media_type + 's']:
            # print(movie)
            try:
                emby_media = self.emby.search(media['name'], media_type)[0]
                # print(emby_media)
                media_metadata = self.emby.get_item_metadata(emby_media['Id'])

                if (media_metadata['UserData']['PlayCount'] > 0):
                    print(f'{media_type} {media["name"]} has already been watched. Skipping...')
                    exclude_media.append(media)
                    continue

                if str(media_metadata['ProductionYear']) == str(media['year'] and media_metadata['Type'] == media_type):
                    # print('match for year')
                    print(f'adding {media_type} to collection {emby_media["Name"]}')
                    self.emby.add_item_to_collection(emby_collection['Id'], emby_media['Id'])

            except Exception as e:
                print(e)
                print(f'--------------------------------------------------------')
                print(f'No match in collection for {media_type} title: {media["name"]} year: {media["year"]}')
                print(f'--------------------------------------------------------')
                radarr = RadarrInteractions(self.config)
                # sonarr = self.config.get_client('sonarr')

                if radarr.client is not None and media_type == 'Movie':
                    radarr.add_movie_by_name_and_year(media['name'], media['year'])

                # if sonarr.client is not None and media_type == 'Series':
                #     sonarr.add_series_by_name(media['name'])

        collection_items, collection_items_count = self.emby.get_items_in_collection(emby_collection['Id'])

        print(collection_items_count, collection_items, count)

        if (collection_items_count < count):
            print('Not enough items in collection. Adding more...', collection_items_count, count)
            time.sleep(20)  # max 3 req per min

            exclude_rule = f'Do not include these {media_type}\'s: {self._convert_media_list_to_names_as_csv(exclude_media)}'
            self.create_emby_ai_recommended(name, media_list, count, media_type, retry_count=retry_count + 1, optional_rules=exclude_rule)

        return emby_collection

    def create_emby_ai_recommended_by_watched(self, name, count=30, media_type="Movie"):
        # get a list of all watched movies
        watched_movies = self.emby.get_movies(limit=10000, is_played=True)

        return self.create_emby_ai_recommended(name, watched_movies, count, media_type)

    def create_emby_ai_recommended_by_collection(self, name, collection_name, count=30, media_type="Movie",
                                                 if_exists_delete=True):
        collection = self.emby.get_collection_by_name(collection_name)
        collection_items, count = self.emby.get_items_in_collection(collection['Id'])

        return self.create_emby_ai_recommended(name, collection_items, count, media_type)

    def create_emby_ai_recommended_by_favorites(self, name, count=30, media_type="Movie", if_exists_delete=True):
        liked_movies = self.emby.get_liked_movies(limit=10000)
        return self.create_emby_ai_recommended(name, liked_movies, count, media_type)

    def create_emby_ai_recommended_by_unwatched(self, name, count=30, media_type="Movie", if_exists_delete=True):
        unwatched_movies = self.emby.get_unwatched_movies(limit=10000)

        return self.create_emby_ai_recommended(name, unwatched_movies, count, media_type,
                                               optional_rules='Only suggest movies from the list I provided.')

    def create_emby_ai_recommended_by_genre(self, name, genre, count=30, media_type="Movie", if_exists_delete=True):
        movies = self.emby.get_movies_by_genre(limit=10000, genre=genre)

        return self.create_emby_ai_recommended(name, movies, count, media_type,
                                               optional_rules=f'Only suggest movies that are part of the genre: {genre}')

    def create_emby_ai_recommended_by_prompt(self, name, prompt, count=30, media_type="Movie", if_exists_delete=True):

        return self.create_emby_ai_recommended(name, count=count, media_type=media_type,
                                               optional_rules=prompt)

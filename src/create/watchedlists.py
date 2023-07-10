import logging
from datetime import datetime


class WatchedListCreator:
    def __init__(self, config):
        self.config = config
        self.plex = config.get_client('plex')
        self.emby = config.get_client('emby')

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
        print('Created Previously Watchedlist')

        print('emby_watchlist', emby_watchlist)

        watchlist_items = self.emby.get_items_in_collection(emby_watchlist['Id'])

        for item in watchlist_items:
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

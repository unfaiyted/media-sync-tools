from config import ConfigManager

config = ConfigManager()

plex = config.get_client('plex')
emby = config.get_client('emby')

# Get all libraries in Plex
plex_libraries = plex.library.sections()

# Set the initial and final years for filtering
start_year = 1900
end_year = 2030

# Loop through the years in batches of 10
for year in range(start_year, end_year + 1, 10):
    print(f"Processing items from {year} to {year + 9}")

    # Loop through all libraries and all items in each library
    for library in plex_libraries:
        print(f"Processing library: {library.title} for {year} to {year + 9}")
        print(library)

        # Filter items based on the year range
        filter = {
            "year>>=": year,
            "year<<=": year + 9
        }

        filtered_items = library.search(filters=filter)

        print(f"Found {len(filtered_items)} items")

        for item in filtered_items:
            print(f"Processing item: {item.title}")

            print(item)

            # Check if the item is a favorite in Plex
            #TODO: Calculate favorite plex does not have this status code
            # Plex does allow for rating of content though 1-5 star.
            # could implement this using the rating attribute
            if item.isFavorite:
                # Search for the item in Emby
                emby_item = emby.search(item.title)[0]
                print('Emby item: ', emby_item)

                # Add the item to Emby favorites
                emby.set_favorite(emby_item['Id'])
                print(f"Added {item.title} to Emby favorites")

    print(f"Finished processing items from {year} to {year + 9}")

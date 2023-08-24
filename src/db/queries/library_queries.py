
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.models import Library, LibraryType


#Get Library with Library Clients
async def get_library_with_clients(db: AsyncIOMotorDatabase, library_id: str) -> Library:
    """
    Retrieve a library and its associated clients.
    """
    pipeline = [
        {
            "$match": {"libraryId": library_id}
        },
        {
            "$lookup": {
                "from": "library_clients",
                "localField": "libraryId",
                "foreignField": "libraryId",
                "as": "clients"
            }
        }
    ]

    libraries = await db.libraries.aggregate(pipeline).to_list(length=1)

    # Since we used to_list, the result is a list. Return the first (and only) element.
    library = Library.parse_obj(libraries[0])

    return library if library else None


async def get_libraries_with_clients_by_config_id(db: AsyncIOMotorDatabase, config_id: str) -> List[Library]:
    """
    Retrieve all libraries and their associated clients by a configuration ID.
    """

    # Use aggregation to combine the libraries with their clients
    pipeline = [
        {
            "$match": {"configId": config_id}
        },
        {
            "$lookup": {
                "from": "library_clients",
                "localField": "libraryId",
                "foreignField": "libraryId",
                "as": "clients"
            }
        }
    ]

    print('pipeline ',pipeline)
    raw_libraries = await db.libraries.aggregate(pipeline).to_list(length=1000)  # Adjust length as necessary

    print('raw_libraries ',raw_libraries)
    # Convert the raw dictionary data into Pydantic Library models
    libraries = [Library.parse_obj(lib) for lib in raw_libraries]

    print('libraries ',libraries)
    return libraries




async def create_library(
    db: AsyncIOMotorDatabase,
    library_name: str,
    library_type: LibraryType,
    client_id: str
) -> Optional[Library]:
    """
    Create a library and assign it to a client.
    """

    # Step 1: Insert a new library into the 'libraries' collection.
    library_data = {
        "name": library_name,
        "type": library_type,
        "configId": "APP-DEFAULT-CONFIG"
    }

    library_result = await db.libraries.insert_one(library_data)

    # If the insertion was not successful, return None
    if not library_result.acknowledged:
        return None

    # Step 2: Create a `LibraryClient` object.
    library_client_data = {
        "libraryId": str(library_result.inserted_id),
        "libraryName": library_name,
        "clientId": client_id
    }
    # This is not strictly necessary but can be useful to return the library with its new id.



    # Step 3: Insert the `LibraryClient` object into the 'library_clients' collection.
    client_result = await db.library_clients.insert_one(library_client_data)

    # If the insertion was not successful, return None
    if not client_result.acknowledged:
        return None

    # Fetch the newly created library from the database for the return value.
    library = await db.libraries.find_one({"_id": library_result.inserted_id})

    # Convert the raw dictionary data into the Pydantic Library model.
    return Library.parse_obj(library)

from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from app.tools import (
    all_in_one, copy_database, create_database, create_db_user, grant_permission,
    create_folder, set_folder_permission, copy_file, copy_files_only, copy_all,
    get_data, insert_data,get_weather
)

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tools = [
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "copy_database",
    #         "description": "Copy database using mysqldump",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "source_db": {"type": "string"},
    #                 "target_db": {"type": "string"},
    #                 "user": {"type": "string"},
    #                 "password": {"type": "string"}
    #             },
    #             "required": ["source_db", "target_db", "user", "password"]
    #         }
    #     }
    # },
    # {
    #     "type":"function",
    #     "function" : {
    #         "name":"create_database",
    #         "description":"create new database",
    #         "parameters":{
    #             "type":"object",
    #             "properties":{
    #                 "db_name":{"type":"string"}
    #             },
    #             "required":["db_name"]
    #         }
    #     }
    # },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "create_db_user",
    #         "description": "Create a new database user",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "db_user": {"type": "string"},
    #                 "db_pass": {"type": "string"},
    #             },
    #             "required": ["db_user", "db_pass"]
    #         }
    #     }
    # },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "grant_permission",
    #         "description": "Grant database permissions to a user",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "db_user": {"type": "string"},
    #                 "db_name": {"type": "string"},
    #             },
    #             "required": ["db_user", "db_name"]
    #         }
    #     }
    # },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "create_folder",
    #         "description": "Create a folder at the specified path",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "path": {"type": "string"}
    #             },
    #             "required": ["path"]
    #         }
    #     }
    # },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "set_folder_permission",
    #         "description": "Set permissions on a folder",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "path": {"type": "string"},
    #                 "permission": {"type": "number"}
    #             },
    #             "required": ["path", "permission"]
    #         }
    #     }
    # },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "copy_file",
    #         "description": "Copy a file from source to destination",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "src": {"type": "string"},
    #                 "dest": {"type": "string"},
    #             },
    #             "required": ["src", "dest"]
    #         }
    #     }
    # },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "copy_files_only",
    #         "description": "Copy all file from source folder to destination folder",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "source_folder": {"type": "string"},
    #                 "destination_folder": {"type": "string"},
    #             },
    #             "required": ["source_folder", "destination_folder"]
    #         }
    #     }
    # },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "copy_all",
    #         "description": "Copy all file from source folder to destination folder",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "source_folder": {"type": "string"},
    #                 "destination_folder": {"type": "string"},
    #             },
    #             "required": ["source_folder", "destination_folder"]
    #         }
    #     }
    # },
    {
        "type": "function",
        "function": {
            "name": "all_in_one",
            "description": "copy_database, create_db_user, grant_permission, create_folder, set_folder_permission and copy_file",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_db": {"type": "string"},
                    "target_db": {"type": "string"},
                    "user": {"type": "string"},
                    "password": {"type": "string"},
                    "db_user": {"type": "string"},
                    "db_pass": {"type": "string"},
                    "path": {"type": "string"},
                    # "permission": {"type": "string"},
                    "src": {"type": "string"},
                    # "dest": {"type": "string"},
                },
                "required": ["source_db", "target_db", 
                            "user", "password",
                            "db_user", "db_pass",  "path", 
                            # "permission",
                            "src", 
                            # "dest"
                            ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_data",
            "description": "get data from database table with optional where clause",
            "parameters": {
                "type": "object",
                "properties": {
                    "database": {"type": "string"},
                    "table": {"type": "string"},
                    "columns": {"type": "string"},
                    "where": {"type": "string"},
                },
                "required": ["database", "table"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "insert_data",
            "description": "insert data into table",
            "parameters": {
                "type": "object",
                "properties": {
                    "database": {"type": "string"},
                    "table": {"type": "string"},
                    "data": {"type": "string"},
                },
                "required": ["database", "table", "data"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
            }
        }
    }
]


def run_agent(query: str):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": query}],
        tools=tools
    )

    message = response.choices[0].message

    # Tool call?
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        fn = globals()[tool_call.function.name]
        arg = tool_call.function.arguments
        result = fn(**json.loads(arg))
        # result = fn(tool_call.function.arguments)
        return result

    # Normal LLM reply
    return message.content

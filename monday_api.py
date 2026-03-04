# Goal: Successfully fetch board data from monday.com
import requests

API_URL = "https://api.monday.com/v2"
API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjYyODYxNDQxNSwiYWFpIjoxMSwidWlkIjoxMDA1NzI3MzksImlhZCI6IjIwMjYtMDMtMDRUMDg6MDA6MTguMTY5WiIsInBlciI6Im1lOndyaXRlIiwiYWN0aWQiOjM0MDY0NDEwLCJyZ24iOiJhcHNlMiJ9.1OFw7dyK95ySuh1fcCqdQUsCHDMYtob-DMqjryxkMjg"

headers = {
    "Authorization": API_TOKEN,
    "Content-Type": "application/json"
}

def get_board_items(board_id):
    query = f"""
    {{
      boards(ids: {board_id}) {{
        items_page {{
          items {{
            name
            column_values {{
              text
              column {{
                title
              }}
            }}
          }}
        }}
      }}
    }}
    """

    response = requests.post(API_URL, json={"query": query}, headers=headers)
    return response.json()
if __name__ == "__main__":
    result = get_board_items(5026984879)  # replace with your board ID
    print(result)
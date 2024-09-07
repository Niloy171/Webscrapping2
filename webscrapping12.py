import requests
from bs4 import BeautifulSoup

def get_actor_filmography_wikipedia(actor_name):
    search_url = f"https://en.wikipedia.org/wiki/{actor_name.replace(' ', '_')}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("Request timed out. The server may be too slow or unreachable.")
        return None, None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return None, None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None, None

    soup = BeautifulSoup(response.content, 'html.parser')

    filmography_section = None
    possible_headings = ['Filmography', 'Career', 'Acting career']
    for heading in possible_headings:
        filmography_section = soup.find('span', {'id': heading})
        if filmography_section:
            break

    if not filmography_section:
        print("Filmography section not found on Wikipedia.")
        return None, None

    movies = []
    filmography_table = filmography_section.find_next('table', class_='wikitable')
  
    if filmography_table:
        rows = filmography_table.find_all('tr')
        for row in rows[1:]:
            cells = row.find_all('td')
            if len(cells) > 1:
                movie_title = cells[0].get_text(strip=True)
                movie_year = cells[1].get_text(strip=True)
                movies.append((movie_title, movie_year))
    else:
        filmography_list = filmography_section.find_next('ul')
        if filmography_list:
            items = filmography_list.find_all('li')
            for item in items:
                text = item.get_text(strip=True)
                parts = text.split('(')
                if len(parts) > 1:
                    movie_title = parts[0].strip()
                    movie_year = parts[-1].split(')')[0].strip()
                    if movie_year.isdigit() and len(movie_year) == 4:
                        movies.append((movie_title, movie_year))
    
    if not movies:
        print(f"No movies found for {actor_name}")
        return None, None

    sorted_movies = sorted(movies, key=lambda x: x[1], reverse=True)
    return actor_name, sorted_movies


def main():
    actor_name = input("Enter the actor's name: ")
    name, movies = get_actor_filmography_wikipedia(actor_name)

    if name and movies:
        print(f"Movies of {name} in descending order:")
        for movie, year in movies:
            print(f"{year} - {movie}")
    else:
        print("Actor not found or filmography section missing.")


if __name__ == "__main__":
    main()

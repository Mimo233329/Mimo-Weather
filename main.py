import python_weather
import datetime
from flet import *
import flet


def main(page: flet.Page):
    # Function to set background based on the current day
    def set_daily_background():
        today = datetime.datetime.now()
        day_of_year = today.timetuple().tm_yday  # Get the day of the year (1-365)

        # Cycle through 7 different backgrounds based on the day of the year
        background_index = day_of_year % 7 
        background_images = [
            "assets/day1.ico",
            "assets/day2.jpg",
            "assets/day3.jpg",
            "assets/day4.jpg",
            "assets/day5.jpg",
            "assets/day6.jpg",
            "assets/day7.jpg",
        ]

        page.bgcolor = colors.TRANSPARENT
        page.decoration = BoxDecoration(
            image=DecorationImage(
                src=background_images[background_index],  # Select image based on day
                fit=ImageFit.COVER,
                opacity=0.3
            )
        )
        page.update()

    async def get_weather(city: str):
        try:
            async with python_weather.Client(unit=python_weather.METRIC) as client:
                weather = await client.get(city)
                current_temp = weather.temperature
                daily = weather.daily_forecasts
                daily_forecast = "\n".join([f"Day {i+1}: {day.date} - {day.temperature}°C" for i, day in enumerate(daily)])
                return f"Current temperature: {current_temp}°C\n{daily_forecast}"
        except Exception as e:
            return f"Error: {str(e)}"

    async def fetch_weather(e):
        city = city_input.value.strip()
        if not city:
            weather_text.value = "Please enter a city name."
            page.update()
            return

        weather_text.value = "Fetching weather data..."
        page.update()

        # Fetch weather data
        weather_data = await get_weather(city)
        weather_text.value = weather_data
        page.update()

    # Set background when the app starts
    set_daily_background()

    # Page properties
    page.title = "Mimo Weather"
    page.window_width = 390
    page.window_height = 740
    page.horizontal_alignment = "center"

    # Title section
    title_section = Container(
        content=Text("Mimo Weather", size=25, color="White"),
        padding=padding.all(10),
        alignment=alignment.top_center,
    )

    # Input field
    city_input = TextField(
        prefix_icon=icons.SEARCH,
        helper_text="e.g., Cairo",
        hint_text="Enter city name",
        color="black",
        expand=True,
    )

    # Weather result display
    weather_text = Text(value="", size=20, color="black")

    # Button to trigger weather update
    check_weather_button = ElevatedButton(
        text="Get Weather",
        on_click=fetch_weather,
    )

    # Layout
    input_section = Container(
        content=Column(
            controls=[
                city_input,
                check_weather_button,
                weather_text,
            ]
        ),
        padding=padding.only(left=10),
        alignment=alignment.top_left,
    )

    # Add sections to the page
    page.add(
        Column(
            controls=[
                title_section,
                input_section,
            ],
            spacing=10,
            alignment="start",
        )
    )


if __name__ == "__main__":
    flet.app(main)

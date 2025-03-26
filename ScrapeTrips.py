import json
import time
from selenium.webdriver.common.by import By


# I know this isn't best practices, and we should be reusing code through functions, but even ChatGPT couldn't produce
# a working version with functions. So for now, let's just focus on making it work. and then focus on best practices later


def scrape_active_trips(driver, scrape_limit=None):
    allTrips = []
    try:
        active_trip_list = driver.find_elements(By.CSS_SELECTOR,
                                                '#active-trip-list-wrapper > ul > li > div.grid_4.overview.borderR_4 > h3 > a')
        print(len(active_trip_list))
        if not active_trip_list:
            print("No active trips found!")
            return

        rangeFortheLoop = len(active_trip_list) if scrape_limit is None else scrape_limit
        for i in range(rangeFortheLoop):
            tripBox = driver.find_elements(By.CSS_SELECTOR, "#active-trip-list-wrapper > ul > li ")
            trip = tripBox[i].find_element(By.CSS_SELECTOR,
                                           ' div.grid_4.overview.borderR_4 > h3 > a')

            if len(tripBox[i].find_elements(By.CSS_SELECTOR, " ul.trip-set>li ")) == 0:
                print(f"no trip items in {trip.text}")
                continue;

            if i >= 4:
                driver.find_element(By.CSS_SELECTOR, "#active-trip-list-wrapper > p.see-more > a").click()
                time.sleep(3)

            trip.click()
            time.sleep(2)

            itinerary = driver.find_element(By.ID, 'itinerary')
            itinerary_list = itinerary.find_elements(By.CSS_SELECTOR, ".itinerary-list")
            allDetails = []
            details = {}
            for list_item in itinerary_list:
                itinerary_list_items = list_item.find_elements(By.XPATH, "./li")

                # Ensure all items inside the drawer are visible
                elements = driver.find_elements(By.CSS_SELECTOR, ".drawer.group")
                for e in elements:
                    driver.execute_script("arguments[0].style.display = 'block';", e)

                for item in itinerary_list_items:
                    what = item.get_attribute("class").split(" ")[1]
                    if what == "air":
                        details = {

                            'type': what,
                            'date': item.find_element(By.XPATH, "../..").find_element(By.CSS_SELECTOR,
                                                                                      "h2.day-itinerary").text,
                            'flightName': item.find_element(By.CSS_SELECTOR, 'div.grid_4.overview.borderR_4 > h3').text,
                            'airports': item.find_element(By.CSS_SELECTOR,
                                                          'div.grid_4.overview.borderR_4 > p').text.strip(),
                            'departureTime': item.find_element(By.CSS_SELECTOR,
                                                               'div.grid_4.overview.borderR_4 > table > tbody > tr:nth-child(2) > td:nth-child(1)').text.strip(),
                            'arrivalTime': item.find_element(By.CSS_SELECTOR,
                                                             'div.grid_4.overview.borderR_4 > table > tbody > tr:nth-child(4) > td:nth-child(1)').text.strip(),
                            'Confirmation Number': item.find_element(By.CSS_SELECTOR,
                                                                     '.drawer.trip-item-drawer.group .grid_4.alpha p:nth-child(1)').text.split(
                                ":")[1].strip(),
                            'Flight Duration': item.find_element(By.CSS_SELECTOR,
                                                                 '.drawer.trip-item-drawer.group .grid_4.alpha p:nth-child(2)').text.split(
                                ":")[1].strip()
                        }
                    elif what == "hotel":
                        details = {
                            'type': what,
                            "hotel": item.find_element(By.CSS_SELECTOR,
                                                       "  div.wrapper > div.grid_4.overview.borderR_4 > h3").text,
                            "location": item.find_element(By.CSS_SELECTOR,
                                                          "div.wrapper > div.grid_4.overview.borderR_4 > p").text,
                            'date': itinerary.find_element(By.CSS_SELECTOR, 'h2.day-itinerary').text.strip(),
                            'checkin': item.find_element(By.CSS_SELECTOR,
                                                         'div.grid_4.overview.borderR_4 > table > tbody > tr:nth-child(2) > td:nth-child(1)').text.strip(),
                            'checkinTime': item.find_element(By.CSS_SELECTOR,
                                                             "div.wrapper > div.grid_4.overview.borderR_4 > table > tbody > tr:nth-child(2) > td:nth-child(2)").text,
                            'checkoutTime': item.find_element(By.CSS_SELECTOR,
                                                              "div.wrapper > div.grid_4.overview.borderR_4 > table > tbody > tr:nth-child(4) > td:nth-child(2)").text,
                            'checkout': item.find_element(By.CSS_SELECTOR,
                                                          'div.grid_4.overview.borderR_4 > table > tbody > tr:nth-child(4) > td:nth-child(1)').text.strip(),
                            'ConfirmationNumber': item.find_element(By.CSS_SELECTOR,
                                                                    '.drawer.trip-item-drawer.group .grid_4.alpha p:nth-child(1)').text.split(
                                ":")[1].strip()
                        }
                    elif what == "cruise":
                        details = {
                            'type': what,
                            "CruiseName": item.find_element(By.CSS_SELECTOR,
                                                            "div.wrapper > div.grid_4.overview.borderR_4 > h3").text,
                            "StartLocation": item.find_element(By.CSS_SELECTOR,
                                                               "div.drawer.trip-item-drawer.group > .alpha> address p").text,
                            "EndLocation": item.find_elements(By.CSS_SELECTOR, "p")[1].text,
                            "StartDate": item.find_element(By.CSS_SELECTOR, "td.start-data.active").text,
                            "StartTime": item.find_element(By.CSS_SELECTOR, "td.start-data.active + td").text,

                            "EndDate": item.find_element(By.CSS_SELECTOR, "td.end-data").text,

                            "EndTime": item.find_element(By.CSS_SELECTOR, "td.end-data + td").text,

                            "ConfirmationNumber": item.find_element(By.CSS_SELECTOR,
                                                                    "div.drawer.trip-item-drawer.group > div:nth-child(3) > p").text.split(
                                ":")[1].strip()
                        }
                    allDetails.append(details)
            name = driver.find_element(By.CSS_SELECTOR, ".trip-name-text").text
            trip_details = {"source": "TripCase Migration", "id": driver.current_url.split("/")[-2], "name": name,
                            "items": allDetails, }

            allTrips.append(trip_details)

            driver.back()
            time.sleep(3)
        # find past Trips
    except Exception as e:
        print(f"Error while checking active trips: {e}")
    finally:
        with open("data.json", "w") as file:
            file.write(json.dumps(allTrips, indent=2))


def scrape_past_trips(driver, scrape_limit=None):
    past_trips_collapsible = driver.find_element(By.XPATH, '//*[@id="past-trip-list"]/a')
    past_trips_collapsible.click()
    elements = driver.find_elements(By.CSS_SELECTOR, "#past-trip-list-wrapper > ul > li.empty-trip-message")

    # Check if the element exists
    if len(elements) != 0:
        print(+elements[0].text)
        return

    allTrips = []
    try:
        past_trips_collapsible = driver.find_element(By.XPATH, '//*[@id="past-trip-list"]/a')

        if "closed" in past_trips_collapsible.get_attribute("class").split(" "):
            past_trips_collapsible.click()
            time.sleep(3)

        driver.find_element(By.XPATH, '//*[@id="past-trip-list-wrapper"]/p/a').click()

        past_trips = driver.find_elements(By.CSS_SELECTOR,
                                          "#past-trip-list-wrapper ul.trip-list >li  div.grid_4.overview.borderR_4 > h3 > a")

        if not past_trips:
            print("No past trips found!")
            return
        print("number of past trips: " + str(len(past_trips)))

        # driver.find_element(By.XPATH, '//*[@id="past-trip-list-wrapper"]/p').click()
        rangeForTheLoop = len(past_trips) if scrape_limit is None else scrape_limit
        for i in range(rangeForTheLoop):

            past_trips_collapsible = driver.find_element(By.XPATH, '//*[@id="past-trip-list"]/a')

            if "closed" in past_trips_collapsible.get_attribute("class").split(" "):
                past_trips_collapsible.click()

                time.sleep(3)

            seemore = driver.find_elements(By.CSS_SELECTOR, '#past-trip-list-wrapper > p.see-more')
            if seemore:
                display_style = seemore[0].value_of_css_property("display")
                if i >= 4 and display_style != "none":
                    seemore[0].find_element(By.TAG_NAME, "a").click()
                    time.sleep(4)
                #
            past_trips_box = driver.find_elements(By.CSS_SELECTOR,
                                                  "#past-trip-list-wrapper ul.trip-list >li")

            trip = past_trips_box[i].find_element(By.CSS_SELECTOR, "div.grid_4.overview.borderR_4 > h3 > a")

            if len(past_trips_box[i].find_elements(By.CSS_SELECTOR, " ul.trip-set>li ")) == 0:
                print(f"no trip items in {trip.text}")
                continue

            trip.click()
            time.sleep(2)

            itinerary = driver.find_element(By.ID, 'itinerary')
            itinerary_list = itinerary.find_elements(By.CSS_SELECTOR, ".itinerary-list")
            allDetails = []
            details = {}
            for list_item in itinerary_list:
                itinerary_list_items = list_item.find_elements(By.XPATH, "./li")
                elements = driver.find_elements(By.CSS_SELECTOR, ".drawer.group")
                for e in elements:
                    driver.execute_script("arguments[0].style.display = 'block';", e)

                for item in itinerary_list_items:
                    what = item.get_attribute("class").split(" ")[1]
                    if what == "air":
                        details = {

                            'type': what,
                            'date': item.find_element(By.XPATH, "../..").find_element(By.CSS_SELECTOR,
                                                                                      "h2.day-itinerary").text,
                            'flightName': item.find_element(By.CSS_SELECTOR, 'div.grid_4.overview.borderR_4 > h3').text,
                            'airports': item.find_element(By.CSS_SELECTOR,
                                                          'div.grid_4.overview.borderR_4 > p').text.strip(),
                            'departureTime': item.find_element(By.CSS_SELECTOR,
                                                               'div.grid_4.overview.borderR_4 > table > tbody > tr:nth-child(2) > td:nth-child(1)').text.strip(),
                            'arrivalTime': item.find_element(By.CSS_SELECTOR,
                                                             'div.grid_4.overview.borderR_4 > table > tbody > tr:nth-child(4) > td:nth-child(1)').text.strip(),
                            'Confirmation Number': item.find_element(By.CSS_SELECTOR,
                                                                     '.drawer.trip-item-drawer.group .grid_4.alpha p:nth-child(1)').text.split(
                                ":")[1].strip(),
                            'Flight Duration': item.find_element(By.CSS_SELECTOR,
                                                                 '.drawer.trip-item-drawer.group .grid_4.alpha p:nth-child(2)').text.split(
                                ":")[1].strip()
                        }
                    elif what == "hotel":
                        details = {
                            'type': what,
                            "hotel": item.find_element(By.CSS_SELECTOR,
                                                       "  div.wrapper > div.grid_4.overview.borderR_4 > h3").text,
                            "location": item.find_element(By.CSS_SELECTOR,
                                                          "div.wrapper > div.grid_4.overview.borderR_4 > p").text,
                            'date': itinerary.find_element(By.CSS_SELECTOR, 'h2.day-itinerary').text.strip(),
                            'checkin': item.find_element(By.CSS_SELECTOR,
                                                         'div.grid_4.overview.borderR_4 > table > tbody > tr:nth-child(2) > td:nth-child(1)').text.strip(),
                            'checkinTime': item.find_element(By.CSS_SELECTOR,
                                                             "div.wrapper > div.grid_4.overview.borderR_4 > table > tbody > tr:nth-child(2) > td:nth-child(2)").text,
                            'checkoutTime': item.find_element(By.CSS_SELECTOR,
                                                              "div.wrapper > div.grid_4.overview.borderR_4 > table > tbody > tr:nth-child(4) > td:nth-child(2)").text,
                            'checkout': item.find_element(By.CSS_SELECTOR,
                                                          'div.grid_4.overview.borderR_4 > table > tbody > tr:nth-child(4) > td:nth-child(1)').text.strip(),
                            'ConfirmationNumber': item.find_element(By.CSS_SELECTOR,
                                                                    '.drawer.trip-item-drawer.group .grid_4.alpha p:nth-child(1)').text.split(
                                ":")[1].strip()
                        }
                    elif what == "cruise":
                        details = {
                            'type': what,
                            "CruiseName": item.find_element(By.CSS_SELECTOR,
                                                            "div.wrapper > div.grid_4.overview.borderR_4 > h3").text,
                            "StartLocation": item.find_element(By.CSS_SELECTOR,
                                                               "div.drawer.trip-item-drawer.group > .alpha> address p").text,
                            "EndLocation": item.find_elements(By.CSS_SELECTOR, "p")[1].text,
                            "StartDate": item.find_element(By.CSS_SELECTOR, "td.start-data.active").text,
                            "StartTime": item.find_element(By.CSS_SELECTOR, "td.start-data.active + td").text,

                            "EndDate": item.find_element(By.CSS_SELECTOR, "td.end-data").text,

                            "EndTime": item.find_element(By.CSS_SELECTOR, "td.end-data + td").text,

                            "ConfirmationNumber": item.find_element(By.CSS_SELECTOR,
                                                                    "div.drawer.trip-item-drawer.group > div:nth-child(3) > p").text.split(
                                ":")[1].strip()
                        }
                    allDetails.append(details)
            name = driver.find_element(By.CSS_SELECTOR, ".trip-name-text").text
            trip_details = {"source": "TripCase Migration", "id": driver.current_url.split("/")[-2], "name": name,
                            "items": allDetails, }

            allTrips.append(trip_details)

            driver.back()
            time.sleep(3)

    except Exception as e:
        raise e
    finally:
        with open("pastTrip.json", "w") as file:
            file.write(json.dumps(allTrips, indent=2))

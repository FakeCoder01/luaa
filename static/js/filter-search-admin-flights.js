

async function GetAvailableFlights(params) {

    $.ajax({
        type: "GET",
        url: "/manage/search/flights/",
        data: params,
        success: function (msg) {
            const response = msg;

            if (response.status_code == 200) {
                document.getElementById("farted_table_flights_data").innerHTML = '';

                for (let i = 0; i < response.flights.length; i++) {
                    const x = response.flights[i];
                    $('#farted_table_flights_data').append(`
                        <tr onclick="window.location.href='/manage/flights/${x.uid}';" class="bg-gray-50 cursor-pointer dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-900 text-gray-700 dark:text-gray-400">   
                            <td class="px-4 py-3 text-sm">${x.flight_number}</td>
                            <td class="px-4 py-3">
                                <div class="flex items-center text-sm">
                                    <div>
                                        <p class="font-semibold">${x.origin_airport.iata_code}</p>
                                        <p class="text-xs text-gray-600 dark:text-gray-400">${x.origin_airport.airport_city}</p>
                                    </div>
                                </div>
                            </td>

                            <td class="px-4 py-3">
                                <div class="flex items-center text-sm">
                                    <div>
                                        <p class="font-semibold">${x.destination_airport.iata_code}</p>
                                        <p class="text-xs text-gray-600 dark:text-gray-400">${x.destination_airport.airport_city}</p>
                                    </div>
                                </div>
                            </td>

                            <td class="px-4 py-3">
                               <div class="flex items-center text-sm">
                                    <div>
                                        <p class="font-semibold">${x.departure_date}</p>
                                        <p class="text-xs text-gray-600 dark:text-gray-400">${x.departure_time}</p>
                                    </div>
                                </div>
                            </td>
                        </tr>

                    `);
                }

            }

        }
    });


}



function SearchAdminFlightFilter() {

    const flight_number_search = document.getElementById('flight_number_search').value;
    const flight_date_search = document.getElementById('flight_date_search').value;
    const flight_time_search = document.getElementById('flight_time_search').value;
    const flight_pad_search = document.getElementById('flight_pad_search').value;

    if (flight_number_search == '' && flight_date_search == '' && flight_time_search == '') {
        document.getElementById("alerts-list").innerHTML += `<div onclick="this.style.display='none';" 
            class="p-2 bg-yellow-200 text-red-500 cursor-pointer font-semibold p-4 text-sm rounded border border-yellow-300 my-3">
                Fill atleast one of the seach field
            </div>`
            ;
        return;
    }


    data = {
        'flight_number_search': flight_number_search,
        'flight_date_search': flight_date_search,
        'flight_time_search': flight_time_search,
        'flight_pad_search': flight_pad_search
    }

    GetAvailableFlights(data)
    return;


}


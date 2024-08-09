


let flight_search_url = "/api/search/flights/";


function sort_filter(){
    const sort_key = $('#sort_key').val();
    if(sort_key === "price" || sort_key === "time" || sort_key === "stops"){
        flight_search_url = "/api/search/flights/?sort_key="+sort_key;
    }
    else{
        flight_search_url = "/api/search/flights/";
    }
    SearchFlight();
    return;
}

async function GetAvailableFlights(params){

    $.ajax({
        type: "GET",
        url: flight_search_url,
        data: params,
        success: function(msg){
            const response = msg;

            if(response.status_code == 200){
                document.getElementById("search-flights").innerHTML = '';
                document.getElementById("flight_count").innerText = response.flights_found;
                if (response.seat_class == 'economy_fare') seat_class = "Economy";
                else if (response.seat_class == 'business_fare') seat_class = "Business";
                else seat_class = "First";
                if(response.flights_found == 0){
                    alert("No flights found")
                    return;
                }
                //// Direct
                for(let i=0; i<response.flights.length; i++){
                    const flight = response.flights[i];
                    $('#search-flights').append(`
                        <div class="p-4">
                            <div class="max-w-full  bg-white flex flex-col rounded overflow-hidden shadow-lg">
                                <div class="flex flex-row items-baseline flex-nowrap bg-red-100 p-2">
                                    <svg viewBox="0 0 64 64" data-testid="tripDetails-bound-plane-icon" pointer-events="all"
                                        aria-hidden="true" class="mt-2 mr-1" role="presentation"
                                        style="fill: rgb(223, 202, 202); height: 0.9rem; width: 0.9rem;">
                                        <path
                                            d="M43.389 38.269L29.222 61.34a1.152 1.152 0 01-1.064.615H20.99a1.219 1.219 0 01-1.007-.5 1.324 1.324 0 01-.2-1.149L26.2 38.27H11.7l-3.947 6.919a1.209 1.209 0 01-1.092.644H1.285a1.234 1.234 0 01-.895-.392l-.057-.056a1.427 1.427 0 01-.308-1.036L1.789 32 .025 19.656a1.182 1.182 0 01.281-1.009 1.356 1.356 0 01.951-.448l5.4-.027a1.227 1.227 0 01.9.391.85.85 0 01.2.252L11.7 25.73h14.5L19.792 3.7a1.324 1.324 0 01.2-1.149A1.219 1.219 0 0121 2.045h7.168a1.152 1.152 0 011.064.615l14.162 23.071h8.959a17.287 17.287 0 017.839 1.791Q63.777 29.315 64 32q-.224 2.685-3.807 4.478a17.282 17.282 0 01-7.84 1.793h-9.016z">
                                        </path>
                                    </svg>
                                    <h1 class="ml-2 uppercase font-bold text-gray-500">Departure</h1>
                                    <p class="ml-2 font-normal text-gray-500">${flight.departure_date}</p>
                                </div>




                                <div class="mt-1 flex justify-start bg-white px-2">
                                    <div class="flex mx-2 ml-6 h8 px-2 flex-row items-baseline rounded-full bg-gray-100 p-1">
                                        <svg viewBox="0 0 64 64" pointer-events="all" aria-hidden="true"
                                            class="etiIcon css-jbc4oa" role="presentation"
                                            style="fill: rgb(102, 102, 102); height: 12px; width: 12px;">
                                            <path
                                                d="M43.389 38.269L29.222 61.34a1.152 1.152 0 01-1.064.615H20.99a1.219 1.219 0 01-1.007-.5 1.324 1.324 0 01-.2-1.149L26.2 38.27H11.7l-3.947 6.919a1.209 1.209 0 01-1.092.644H1.285a1.234 1.234 0 01-.895-.392l-.057-.056a1.427 1.427 0 01-.308-1.036L1.789 32 .025 19.656a1.182 1.182 0 01.281-1.009 1.356 1.356 0 01.951-.448l5.4-.027a1.227 1.227 0 01.9.391.85.85 0 01.2.252L11.7 25.73h14.5L19.792 3.7a1.324 1.324 0 01.2-1.149A1.219 1.219 0 0121 2.045h7.168a1.152 1.152 0 011.064.615l14.162 23.071h8.959a17.287 17.287 0 017.839 1.791Q63.777 29.315 64 32q-.224 2.685-3.807 4.478a17.282 17.282 0 01-7.84 1.793h-9.016z">
                                            </path>
                                        </svg>
                                        <p class="font-normal text-sm ml-1 text-red-500 pr-1">${seat_class}</p>
                                    </div>
                                </div>
                                <div class="mt-1 flex sm:flex-row mx-6 sm:justify-between flex-wrap ">


                                    <div class="flex flex-col p-2">
                                        <p class="font-bold">${flight.departure_time}</p> 
                                        <p class="text-gray-500"><span class="font-bold">${flight.origin_airport.iata_code}</span> ${flight.origin_airport.airport_city}</p>
                                        <p class="text-gray-500">${flight.origin_airport.airport_country}</p>
                                    </div>

                                    <div class="flex flex-row place-items-center px-2">
                                        <img alt="Luaa Airways" class="w-10 h-10" 
                                            src="/static/images/logo/logo-icon-without-bg.png"
                                            style="opacity: 1; transform-origin: 0% 50% 0px; transform: none;" />
                                        <div class="flex flex-col ml-2">
                                            <p class="text-xs text-gray-500 font-bold">Luaa Airways</p>
                                            <p class="text-xs text-gray-500">${flight.flight_number}</p>
                                            <div class="text-xs text-gray-500">
                                                ${ Math.trunc(flight.flight_duration / 3600)} hours 
                                                ${ Math.trunc((flight.flight_duration % 3600) / 60)} minutes
                                                 
                                            </div>
                                        </div>
                                    </div>

                                    <div class="flex flex-col flex-wrap px-2">
                                        <p class="font-bold">${flight.arrival_time}</p>
                                        <p class="text-gray-500"><span class="font-bold">${flight.destination_airport.iata_code}</span> ${flight.destination_airport.airport_city}</p>
                                        <p class="text-gray-500">${flight.destination_airport.airport_country}</p>
                                    </div>
                                </div>
                                <div
                                    class="mt-2 bg-red-100 flex flex-row flex-wrap md:flex-nowrap justify-between items-baseline">
                                    <div class="flex mx-6 py-2 flex-row flex-wrap"> </div>
                                    <div
                                        class="md:border-l-2 border-gray-400 mx-6 md:border-dotted flex flex-row py-2 mr-6 flex-wrap">

                                        <svg class="cursor-pointer w-12 h-10 p-2 mx-2 self-center bg-red-300 rounded-full fill-current text-white"
                                            viewBox="0 0 64 64" pointer-events="all" aria-hidden="true" role="presentation">
                                            <path
                                                d="M43.389 38.269L29.222 61.34a1.152 1.152 0 01-1.064.615H20.99a1.219 1.219 0 01-1.007-.5 1.324 1.324 0 01-.2-1.149L26.2 38.27H11.7l-3.947 6.919a1.209 1.209 0 01-1.092.644H1.285a1.234 1.234 0 01-.895-.392l-.057-.056a1.427 1.427 0 01-.308-1.036L1.789 32 .025 19.656a1.182 1.182 0 01.281-1.009 1.356 1.356 0 01.951-.448l5.4-.027a1.227 1.227 0 01.9.391.85.85 0 01.2.252L11.7 25.73h14.5L19.792 3.7a1.324 1.324 0 01.2-1.149A1.219 1.219 0 0121 2.045h7.168a1.152 1.152 0 011.064.615l14.162 23.071h8.959a17.287 17.287 0 017.839 1.791Q63.777 29.315 64 32q-.224 2.685-3.807 4.478a17.282 17.282 0 01-7.84 1.793h-9.016z">
                                            </path>
                                        </svg>
                                        <div class="text-sm mx-2 flex flex-col">
                                            <p class="font-bold">Rs. ${flight.flight_price}</p>
                                            <p class="text-xs text-gray-500">Price per adult</p>
                                        </div>
                                        <button onclick="window.location.href = '/flight/${flight.flight_id}/';"
                                            class="w-32 h-11 rounded flex border-solid border text-white bg-red-500 hover:bg-red-400 mx-2 justify-center place-items-center">
                                            <div class="">Book</div>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `);
                }
                //// Connecting
                for(let i=0; i<response.connecting_flights.length; i++){
                    const flight = response.connecting_flights[i];
                    $('#search-flights').append(`
                        <div class="p-4 bg-green-200 rounded m-4">

                            <!-- FIRST FLIGHT -->
                            <div class="max-w-full  bg-white flex flex-col rounded overflow-hidden shadow-lg">
                                <div class="flex flex-row items-baseline flex-nowrap bg-red-100 p-2">
                                    <svg viewBox="0 0 64 64" data-testid="tripDetails-bound-plane-icon" pointer-events="all"
                                        aria-hidden="true" class="mt-2 mr-1" role="presentation"
                                        style="fill: rgb(223, 202, 202); height: 0.9rem; width: 0.9rem;">
                                        <path
                                            d="M43.389 38.269L29.222 61.34a1.152 1.152 0 01-1.064.615H20.99a1.219 1.219 0 01-1.007-.5 1.324 1.324 0 01-.2-1.149L26.2 38.27H11.7l-3.947 6.919a1.209 1.209 0 01-1.092.644H1.285a1.234 1.234 0 01-.895-.392l-.057-.056a1.427 1.427 0 01-.308-1.036L1.789 32 .025 19.656a1.182 1.182 0 01.281-1.009 1.356 1.356 0 01.951-.448l5.4-.027a1.227 1.227 0 01.9.391.85.85 0 01.2.252L11.7 25.73h14.5L19.792 3.7a1.324 1.324 0 01.2-1.149A1.219 1.219 0 0121 2.045h7.168a1.152 1.152 0 011.064.615l14.162 23.071h8.959a17.287 17.287 0 017.839 1.791Q63.777 29.315 64 32q-.224 2.685-3.807 4.478a17.282 17.282 0 01-7.84 1.793h-9.016z">
                                        </path>
                                    </svg>
                                    <h1 class="ml-2 uppercase font-bold text-gray-500">Departure</h1>
                                    <p class="ml-2 font-normal text-gray-500">${flight.first_flight.departure_date}</p>
                                </div>




                                <div class="mt-1 flex justify-start bg-white px-2">
                                    <div class="flex mx-2 ml-6 h8 px-2 flex-row items-baseline rounded-full bg-gray-100 p-1">
                                        <svg viewBox="0 0 64 64" pointer-events="all" aria-hidden="true"
                                            class="etiIcon css-jbc4oa" role="presentation"
                                            style="fill: rgb(102, 102, 102); height: 12px; width: 12px;">
                                            <path
                                                d="M43.389 38.269L29.222 61.34a1.152 1.152 0 01-1.064.615H20.99a1.219 1.219 0 01-1.007-.5 1.324 1.324 0 01-.2-1.149L26.2 38.27H11.7l-3.947 6.919a1.209 1.209 0 01-1.092.644H1.285a1.234 1.234 0 01-.895-.392l-.057-.056a1.427 1.427 0 01-.308-1.036L1.789 32 .025 19.656a1.182 1.182 0 01.281-1.009 1.356 1.356 0 01.951-.448l5.4-.027a1.227 1.227 0 01.9.391.85.85 0 01.2.252L11.7 25.73h14.5L19.792 3.7a1.324 1.324 0 01.2-1.149A1.219 1.219 0 0121 2.045h7.168a1.152 1.152 0 011.064.615l14.162 23.071h8.959a17.287 17.287 0 017.839 1.791Q63.777 29.315 64 32q-.224 2.685-3.807 4.478a17.282 17.282 0 01-7.84 1.793h-9.016z">
                                            </path>
                                        </svg>
                                        <p class="font-normal text-sm ml-1 text-red-500 pr-1">${seat_class}</p>
                                    </div>
                                </div>
                                <div class="mt-1 flex sm:flex-row mx-6 sm:justify-between flex-wrap ">


                                    <div class="flex flex-col p-2">
                                        <p class="font-bold">${flight.first_flight.departure_time}</p> 
                                        <p class="text-gray-500"><span class="font-bold">${flight.first_flight.origin_airport.iata_code}</span> ${flight.first_flight.origin_airport.airport_city}</p>
                                        <p class="text-gray-500">${flight.first_flight.origin_airport.airport_country}</p>
                                    </div>

                                    <div class="flex flex-row place-items-center px-2">
                                        <img alt="Luaa Airways" class="w-10 h-10" 
                                            src="/static/images/logo/logo-icon.png"
                                            style="opacity: 1; transform-origin: 0% 50% 0px; transform: none;" />
                                        <div class="flex flex-col ml-2">
                                            <p class="text-xs text-gray-500 font-bold">Luaa Airways</p>
                                            <p class="text-xs text-gray-500">${flight.first_flight.flight_number}</p>
                                            <div class="text-xs text-gray-500">
                                                ${ Math.trunc(flight.first_flight.flight_duration / 3600)} hours 
                                                ${ Math.trunc((flight.first_flight.flight_duration % 3600) / 60)} minutes
                                                 
                                            </div>
                                        </div>
                                    </div>

                                    <div class="flex flex-col flex-wrap px-2">
                                        <p class="font-bold">${flight.first_flight.arrival_time}</p>
                                        <p class="text-gray-500"><span class="font-bold">${flight.first_flight.destination_airport.iata_code}</span> ${flight.first_flight.destination_airport.airport_city}</p>
                                        <p class="text-gray-500">${flight.first_flight.destination_airport.airport_country}</p>
                                    </div>
                                </div>
                                <div
                                    class="mt-2 bg-red-100 flex flex-row flex-wrap md:flex-nowrap justify-between items-baseline">
                                    <div class="flex mx-6 py-2 flex-row flex-wrap"> </div>
                                    <div
                                        class="md:border-l-2 border-gray-400 mx-6 md:border-dotted flex flex-row py-2 mr-6 flex-wrap">

                                        <svg class="cursor-pointer w-12 h-10 p-2 mx-2 self-center bg-red-300 rounded-full fill-current text-white"
                                            viewBox="0 0 64 64" pointer-events="all" aria-hidden="true" role="presentation">
                                            <path
                                                d="M43.389 38.269L29.222 61.34a1.152 1.152 0 01-1.064.615H20.99a1.219 1.219 0 01-1.007-.5 1.324 1.324 0 01-.2-1.149L26.2 38.27H11.7l-3.947 6.919a1.209 1.209 0 01-1.092.644H1.285a1.234 1.234 0 01-.895-.392l-.057-.056a1.427 1.427 0 01-.308-1.036L1.789 32 .025 19.656a1.182 1.182 0 01.281-1.009 1.356 1.356 0 01.951-.448l5.4-.027a1.227 1.227 0 01.9.391.85.85 0 01.2.252L11.7 25.73h14.5L19.792 3.7a1.324 1.324 0 01.2-1.149A1.219 1.219 0 0121 2.045h7.168a1.152 1.152 0 011.064.615l14.162 23.071h8.959a17.287 17.287 0 017.839 1.791Q63.777 29.315 64 32q-.224 2.685-3.807 4.478a17.282 17.282 0 01-7.84 1.793h-9.016z">
                                            </path>
                                        </svg>
                                        <div class="text-sm mx-2 flex flex-col">
                                            <p class="font-bold">Rs. ${flight.first_flight.flight_price}</p>
                                            <p class="text-xs text-gray-500">Price per adult</p>
                                        </div>
                                        <button onclick="window.location.href = '/flight/${flight.first_flight.flight_id}/';"
                                            class="w-32 h-11 rounded flex border-solid border text-white bg-red-500 hover:bg-red-400 mx-2 justify-center place-items-center">
                                            <div class="">Book</div>
                                        </button>
                                    </div>
                                </div>
                            </div>



                            <!-- SECOND -->

                            <br>

                            <div class="max-w-full  bg-white flex flex-col rounded overflow-hidden shadow-lg">
                                <div class="flex flex-row items-baseline flex-nowrap bg-red-100 p-2">
                                    <svg viewBox="0 0 64 64" data-testid="tripDetails-bound-plane-icon" pointer-events="all"
                                        aria-hidden="true" class="mt-2 mr-1" role="presentation"
                                        style="fill: rgb(223, 202, 202); height: 0.9rem; width: 0.9rem;">
                                        <path
                                            d="M43.389 38.269L29.222 61.34a1.152 1.152 0 01-1.064.615H20.99a1.219 1.219 0 01-1.007-.5 1.324 1.324 0 01-.2-1.149L26.2 38.27H11.7l-3.947 6.919a1.209 1.209 0 01-1.092.644H1.285a1.234 1.234 0 01-.895-.392l-.057-.056a1.427 1.427 0 01-.308-1.036L1.789 32 .025 19.656a1.182 1.182 0 01.281-1.009 1.356 1.356 0 01.951-.448l5.4-.027a1.227 1.227 0 01.9.391.85.85 0 01.2.252L11.7 25.73h14.5L19.792 3.7a1.324 1.324 0 01.2-1.149A1.219 1.219 0 0121 2.045h7.168a1.152 1.152 0 011.064.615l14.162 23.071h8.959a17.287 17.287 0 017.839 1.791Q63.777 29.315 64 32q-.224 2.685-3.807 4.478a17.282 17.282 0 01-7.84 1.793h-9.016z">
                                        </path>
                                    </svg>
                                    <h1 class="ml-2 uppercase font-bold text-gray-500">Departure</h1>
                                    <p class="ml-2 font-normal text-gray-500">${flight.final_flight.departure_date}</p>
                                </div>




                                <div class="mt-1 flex justify-start bg-white px-2">
                                    <div class="flex mx-2 ml-6 h8 px-2 flex-row items-baseline rounded-full bg-gray-100 p-1">
                                        <svg viewBox="0 0 64 64" pointer-events="all" aria-hidden="true"
                                            class="etiIcon css-jbc4oa" role="presentation"
                                            style="fill: rgb(102, 102, 102); height: 12px; width: 12px;">
                                            <path
                                                d="M43.389 38.269L29.222 61.34a1.152 1.152 0 01-1.064.615H20.99a1.219 1.219 0 01-1.007-.5 1.324 1.324 0 01-.2-1.149L26.2 38.27H11.7l-3.947 6.919a1.209 1.209 0 01-1.092.644H1.285a1.234 1.234 0 01-.895-.392l-.057-.056a1.427 1.427 0 01-.308-1.036L1.789 32 .025 19.656a1.182 1.182 0 01.281-1.009 1.356 1.356 0 01.951-.448l5.4-.027a1.227 1.227 0 01.9.391.85.85 0 01.2.252L11.7 25.73h14.5L19.792 3.7a1.324 1.324 0 01.2-1.149A1.219 1.219 0 0121 2.045h7.168a1.152 1.152 0 011.064.615l14.162 23.071h8.959a17.287 17.287 0 017.839 1.791Q63.777 29.315 64 32q-.224 2.685-3.807 4.478a17.282 17.282 0 01-7.84 1.793h-9.016z">
                                            </path>
                                        </svg>
                                        <p class="font-normal text-sm ml-1 text-red-500 pr-1">${seat_class}</p>
                                    </div>
                                </div>
                                <div class="mt-1 flex sm:flex-row mx-6 sm:justify-between flex-wrap ">


                                    <div class="flex flex-col p-2">
                                        <p class="font-bold">${flight.final_flight.departure_time}</p> 
                                        <p class="text-gray-500"><span class="font-bold">${flight.final_flight.origin_airport.iata_code}</span> ${flight.final_flight.origin_airport.airport_city}</p>
                                        <p class="text-gray-500">${flight.final_flight.origin_airport.airport_country}</p>
                                    </div>

                                    <div class="flex flex-row place-items-center px-2">
                                        <img alt="Luaa Airways" class="w-10 h-10" 
                                            src="/static/images/logo/logo-icon.png"
                                            style="opacity: 1; transform-origin: 0% 50% 0px; transform: none;" />
                                        <div class="flex flex-col ml-2">
                                            <p class="text-xs text-gray-500 font-bold">Luaa Airways</p>
                                            <p class="text-xs text-gray-500">${flight.final_flight.flight_number}</p>
                                            <div class="text-xs text-gray-500">
                                                ${ Math.trunc(flight.final_flight.flight_duration / 3600)} hours 
                                                ${ Math.trunc((flight.final_flight.flight_duration % 3600) / 60)} minutes
                                                
                                            </div>
                                        </div>
                                    </div>

                                    <div class="flex flex-col flex-wrap px-2">
                                        <p class="font-bold">${flight.final_flight.arrival_time}</p>
                                        <p class="text-gray-500"><span class="font-bold">${flight.final_flight.destination_airport.iata_code}</span> ${flight.final_flight.destination_airport.airport_city}</p>
                                        <p class="text-gray-500">${flight.final_flight.destination_airport.airport_country}</p>
                                    </div>
                                </div>
                                <div
                                    class="mt-2 bg-red-100 flex flex-row flex-wrap md:flex-nowrap justify-between items-baseline">
                                    <div class="flex mx-6 py-2 flex-row flex-wrap"> </div>
                                    <div
                                        class="md:border-l-2 border-gray-400 mx-6 md:border-dotted flex flex-row py-2 mr-6 flex-wrap">

                                        <svg class="cursor-pointer w-12 h-10 p-2 mx-2 self-center bg-red-300 rounded-full fill-current text-white"
                                            viewBox="0 0 64 64" pointer-events="all" aria-hidden="true" role="presentation">
                                            <path
                                                d="M43.389 38.269L29.222 61.34a1.152 1.152 0 01-1.064.615H20.99a1.219 1.219 0 01-1.007-.5 1.324 1.324 0 01-.2-1.149L26.2 38.27H11.7l-3.947 6.919a1.209 1.209 0 01-1.092.644H1.285a1.234 1.234 0 01-.895-.392l-.057-.056a1.427 1.427 0 01-.308-1.036L1.789 32 .025 19.656a1.182 1.182 0 01.281-1.009 1.356 1.356 0 01.951-.448l5.4-.027a1.227 1.227 0 01.9.391.85.85 0 01.2.252L11.7 25.73h14.5L19.792 3.7a1.324 1.324 0 01.2-1.149A1.219 1.219 0 0121 2.045h7.168a1.152 1.152 0 011.064.615l14.162 23.071h8.959a17.287 17.287 0 017.839 1.791Q63.777 29.315 64 32q-.224 2.685-3.807 4.478a17.282 17.282 0 01-7.84 1.793h-9.016z">
                                            </path>
                                        </svg>
                                        <div class="text-sm mx-2 flex flex-col">
                                            <p class="font-bold">Rs. ${flight.final_flight.flight_price}</p>
                                            <p class="text-xs text-gray-500">Price per adult</p>
                                        </div>
                                        <button onclick="window.location.href = '/flight/${flight.final_flight.flight_id}/';"
                                            class="w-32 h-11 rounded flex border-solid border text-white bg-red-500 hover:bg-red-400 mx-2 justify-center place-items-center">
                                            <div class="">Book</div>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `);
                }
            }

        }
    });


}



function SearchFlight(){
    const origin = document.getElementById('origin').value;
    const destination = document.getElementById('destination').value;
    const departure_date = document.getElementById('departure_date').value;
    // const return_date = document.getElementById('return_date').value;

    if(origin == '' || destination == '' || departure_date == ''){
        document.getElementById("alerts-list").innerHTML +=  `<div onclick="this.style.display='none';" 
            class="p-2 bg-yellow-200 text-red-500 cursor-pointer font-semibold p-4 text-sm rounded border border-yellow-300 my-3">
                Fill all the fields
            </div>`
        ;
        return;
    }

    if(origin == destination  ){
        document.getElementById("alerts-list").innerHTML +=  `<div onclick="this.style.display='none';" 
            class="p-2 bg-yellow-200 text-red-500 cursor-pointer font-semibold p-4 text-sm rounded border border-yellow-300 my-3">
                Origin and Destination can not be same
            </div>`
        ;
        return;
    }
    // const origin_airport_id = document.getElementById('origin_airport_id').value;
    // const destination_airport_id = document.getElementById('destination_airport_id').value;
    // if(origin_airport_id == '' || destination_airport_id == ''){
    //     window.location.reload();
    // }

    const return_flight = document.getElementById('return_flight').value;
    const seat_class = document.getElementById('seat_class').value;
    const flight_type = document.getElementById('flight_type').value;

    /// i really dont want this one
    const departure_time = document.getElementById('departure_time').value;

    if(return_flight == '' || seat_class == '' || flight_type == ''){
        document.getElementById("alerts-list").innerHTML +=  `<div onclick="this.style.display='none';" 
            class="p-2 bg-yellow-200 text-red-500 cursor-pointer font-semibold p-4 text-sm rounded border border-yellow-300 my-3">
                Fill all the fields
            </div>`
        ;
    }

    
    data = {
        'origin' : origin,
        'destination' : destination,
        'departure_date' : departure_date,
        'return_flight' : return_flight,
        'seat_class' : seat_class,
        'flight_type' : flight_type,
        'departure_time' : departure_time
    }

    GetAvailableFlights(data)
    return;


}

async function AirportFillUp(e){
    const response = await fetch('/api/search/airports?airport_search='+e);
    const airport_search = await response.json()
    const airports = airport_search.airports;
    return airports;
}



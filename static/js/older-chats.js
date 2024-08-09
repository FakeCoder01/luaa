async function ShowOlderChatMessage(chat_id){
    const response = await fetch('/support/both/older-message?chat_id='+chat_id);
    const data = await response.json();
    const chat_groups = JSON.parse(data);
    if(chat_groups.status_code == 200){
        const chats = chat_groups.chats;
        if (chats.length > 0){
            for(let i=0; i<chats.length; i++){
                let messages = document.getElementById('messages');
                const older_message = chats[i];
                if(client_type === 'u'){
                    if (older_message.sender === 'user'){
                        messages.insertAdjacentHTML('afterbegin', 
                            `<div class="flex w-full mt-2 space-x-3 max-w-xs ml-auto justify-end">
                                <div>
                                    <div class="bg-red-600 text-white p-3 rounded-l-lg rounded-br-lg">
                                        <p class="text-sm">${older_message.message} </p>
                                    </div>
                                    <span class="text-xs text-gray-500 leading-none">2 min ago</span>
                                </div>
                                <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300"></div>
                            </div>`
                        );
                    }
                    else if(older_message.sender === 'manager'){
                        messages.insertAdjacentHTML('afterbegin',
                            `<div class="flex w-full mt-2 space-x-3 max-w-xs">
                                <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                                    <img src="{% static '/images/logo/logo-icon.png' %}" alt="Icon" class="h-10 w-10 rounded-full" srcset="">
                                </div>
                                <div>
                                    <div class="bg-gray-300 p-3 rounded-r-lg rounded-bl-lg">
                                        <p class="text-sm">${older_message.message}</p>
                                    </div>
                                    <span class="text-xs text-gray-500 leading-none">2 min ago</span>
                                </div>
                            </div> `
                        );
                    }
                    else{

                    }
                }else if(client_type === 'm'){
                    if (older_message.sender === 'manager') {
                        messages.insertAdjacentHTML('afterbegin',
                            `<div class="flex w-full mt-2 space-x-3 max-w-xs ml-auto justify-end">
                                <div>
                                    <div class="bg-red-600 text-white p-3 rounded-l-lg rounded-br-lg">
                                         <p class="text-sm">${older_message.message} </p>
                                    </div>
                                    <span class="text-xs text-gray-500 leading-none">2 min ago</span>
                                </div>
                                <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                                    <img src="{% static '/images/logo/logo-icon.png' %}" alt="Icon" class="h-10 w-10 rounded-full" srcset="">
                                </div>
                            </div>`
                        );
                    }
                    else if (older_message.sender === 'user') {
                        messages.insertAdjacentHTML('afterbegin',
                            `<div class="flex w-full mt-2 space-x-3 max-w-xs">
                                <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300"></div>
                                <div>
                                    <div class="bg-gray-300 p-3 rounded-r-lg rounded-bl-lg">
                                        <p class="text-sm">${older_message.message}</p>
                                    </div>
                                    <span class="text-xs text-gray-500 leading-none">2 min ago</span>
                                </div>
                            </div> `
                        );
                    }
                    else {
                    }
                }
            }
        }
    } 
    document.getElementById('old-btn').disabled = true;

}
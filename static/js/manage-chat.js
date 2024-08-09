    var show_page = 0;
        var x = 0;

        async function ChatGroupShowAndRefresh() {
            $("#chat-message-group-list-area").html('');
            const response = await fetch('/manage/support/m/group/?show=' + show_page);
            const data = await response.json();
            const chat_groups = JSON.parse(data);
            if(chat_groups.status_code == 200){
                const chats = chat_groups.chats;
                if (chats.length > 0){
                    for(let i=0; i<chats.length; i++){
                        $("#chat-message-group-list-area").append(`
                            <a href="/manage/support/m/${chats[i].profile_id}#siview"> <li class="bg-gray-300 flex flex-row mb-2 rounded-lg px-1">
                                 <div
                                    class="select-none cursor-pointer bg-gray-200 rounded-md flex flex-1 items-center  transition duration-500 ease-in-out transform hover:-translate-y-1 hover:shadow-lg">
                                
                                    <div class="flex-1 pl-1 mr-16">
                                        <div class="font-medium">${chats[i].name}</div> 
                                        <div style="overflow:hidden" class="text-gray-600 text-sm">${chats[i].message}</div>
                                    </div>
                                    <div class="text-gray-600 text-xs">${chats[i].sent_at}</div>
                                </div>
                            </li></a>
                        `);
                    }
                }
                else{
                    $("#chat-message-group-list-area").append(`
                        <li class="bg-gray-300 flex flex-row mb-2 rounded-lg px-1">
                            <h3>No support messages</h3>
                        </li>
                    `);
                }
            }
            else{
                $("#chat-message-group-list-area").append(`
                    <li class="bg-gray-300 flex flex-row mb-2 rounded-lg px-1">
                         <h3>Something went wrong</h3>
                    </li>
                `);
            }
            return;
        }
        ChatGroupShowAndRefresh();
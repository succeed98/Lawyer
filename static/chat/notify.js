let messageList = $("#messages");
const api_path = "";
function drawMessage(message) {
  let position = "left";
  // const date = new Date(message.timestamp);
  if (message.user === currentUser) position = "right";
  const messageItem = `
              <li class="message">
                  <div class="avatar">${message.user}</div>
                      <div class="text_wrapper">
                          <div class="text">${message.body}<br>
                              <span class="small">${message.timestamp}</span>
                      </div>
                  </div>
              </li>`;
  $(messageItem).appendTo("#messages");
}

function getConversation(currentUser) {
  $.getJSON(`chat/api/v1/message/?target=${currentUser}`, function (data) {
    // messageList.children(".message").remove();
    // for (let i = data["results"].length - 1; i >= 0; i--) {
    //   //   drawMessage(data["results"][i]);
    //   console.log(data["results"][i]);
    //   console.log("heloooooooooooooooo");
    // }

    console.log(data);

    // for (let i = 0; i < data.length; i++) {cls
    //   const userItem = `<a class="list-group-item user">${data[i]["username"]}</a>`;
    //   $(userItem).appendTo("#user-list");
    // }
    // messageList.animate({ scrollTop: messageList.prop("scrollHeight") });
  });
}

// function setCurrentRecipient(username) {
//   currentRecipient = username;
//   getConversation(currentRecipient);

// }

$(document).ready(function () {
  getConversation(currentUser);

  disableInput();

  var socket = new WebSocket(
    "ws://" + window.location.host + "/ws?session_key=${sessionKey}"
  );
});

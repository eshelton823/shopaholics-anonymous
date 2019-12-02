$(function() {
  Notification.requestPermission().then(function(result) {
    console.log(result);
  });
  // Reference to the chat messages area
  let $chatWindow = $("#messages");

  // Our interface to the Chat client
  let chatClient;

  // A handle to the room's chat channel
  let roomChannel;

  // The server will assign the client a random username - stored here
  let username;

  // Helper function to print info messages to the chat window
  function print(infoMessage, asHtml) {
    let $msg = $('<div class="info">');
    if (asHtml) {
      $msg.html(infoMessage);
    } else {
      $msg.text(infoMessage);
    }
    $chatWindow.append($msg);
  }

// Helper function to print chat message to the chat window
 function printMessage(fromUser, message, onLoad) {
   let $user = $('<span class="username">').text(fromUser + ":");
   if (fromUser === username) {
     $user.addClass("me");
   }
   let $message = $('<span class="message">').text(message);
   let $container = $('<div class="message-container">');
   $container.append($user).append($message);
   $chatWindow.append($container);
   $chatWindow.scrollTop($chatWindow[0].scrollHeight);
   if(onLoad == false){
     if(Notification.permission === "granted" && fromUser !== username){
       console.log("Notifying.");
       var notification = new Notification("New message from " +fromUser+": "+message);
     }
     // Otherwise, we need to ask the user for permission
     else if (Notification.permission === "denied") {
       Notification.requestPermission().then(function (permission) {
         // If the user accepts, let's create a notification
        if (permission === "granted") {
          var notification = new Notification("New message: "+message);
        }
      });
    }
   }
 }

  // Get an access token for the current user, passing a device ID
  // for browser-based apps, we'll just use the value "browser"
  $.getJSON(
    "/token",
    {
      device: "browser"
    },
    function(data) {
      // Alert the user they have been assigned a random username
      username = data.identity;
      print(
        "Welcome " +
          '<span class="me">' +
          username +
          "</span>!",
        true
      );

      // Initialize the Chat client
      Twilio.Chat.Client.create(data.token).then(client => {
        // Use client
        chatClient = client;
        chatClient.getSubscribedChannels().then(createOrJoinChannel);
      });

    }
  );

  function createOrJoinChannel() {
  // Extract the room's channel name from the page URL
  let channelName = window.location.pathname.split("/").slice(-2, -1)[0];

  chatClient
    .getChannelByUniqueName(channelName)
    .then(function(channel) {
      roomChannel = channel;
      setupChannel(channelName);
    })
    .catch(function() {
      // If it doesn't exist, let's create it
      chatClient
        .createChannel({
          uniqueName: channelName,
          friendlyName: `${channelName} Chat Channel`
        })
        .then(function(channel) {
          roomChannel = channel;
          setupChannel(channelName);
        });
    });
    }

    // Set up channel after it has been found / created
function setupChannel(name) {
  try{
    if(roomChannel.state.status !== "joined"){
      roomChannel.join().then(function(channel) {
        print(
          `Created and joined channel!`,
          true
        );
      });
    }
    else{
      roomChannel.getMessages(30).then(processPage);
    }
  }
  catch{
    console.log("Failed to join on normal route.")
  }

  // Listen for new messages sent to the channel
  roomChannel.on("messageAdded", function(message) {
    printMessage(message.author, message.body, false);
  });
}
function processPage(page) {
  console.log("Processing...");
  page.items.forEach(message => {
    printMessage(message.author, message.body, true);
  });
  if (page.hasNextPage) {
    page.nextPage().then(processPage);
  } else {
    console.log("Done loading messages");
  }
}

let $form = $("#message-form");
let $input = $("#message-input");
$form.on("submit", function(e) {
  e.preventDefault();
  if (roomChannel && $input.val().trim().length > 0) {
    roomChannel.sendMessage($input.val());
    $input.val("");
  }
});
$form.on(‘keypress’,function(e) {
  if (e.which == 13) {
    if (roomChannel && $input.val().trim().length > 0) {
        roomChannel.sendMessage($input.val());
        $input.val(“”);
    }
  }
});
});

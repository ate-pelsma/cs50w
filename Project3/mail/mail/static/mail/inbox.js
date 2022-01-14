document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-form').onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#emails-specific').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-specific').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Load the emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails);
    emails.forEach(email => load_email(email, mailbox));
  });
}

// Sent email function
// Listens for form to be submitted
function send_email() {
  //Create variables from the submitted form
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // Send request to API
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
  .then(response => response.json())
  .then(result => {
    console.log(result);
  })
  .catch(error => {
    console.log('Error', error);
  });

  localStorage.clear();
  load_mailbox('sent');
  return false;
}

function load_email(email, mailbox) {

  // Create a card for each email
  const mailCard = document.createElement('div');
  mailCard.id = "mail-card";
  if (email.read) {
    mailCard.className = "card p-3";
    mailCard.style.backgroundColor = "lightgrey";
  } else {
    mailCard.className = "card p-3";
  }
  // Add each card to the email view
  document.querySelector('#emails-view').append(mailCard);

  // Insert all the necessary things into a div
  const mailDiv = document.createElement('div');
  mailDiv.id = "email";
  mailDiv.className = "row";
  mailCard.append(mailDiv);

  const recipient = document.createElement('div');
  recipient.id = "email-recipient";
  recipient.className = "col-lg-2 col-md-3 col-sm-12 font-weight-bold";
  console.log(`Current mailbox: ${mailbox}`);
  if (mailbox === "sent") {
    recipient.innerHTML = email.recipients[0];
  } else {
    recipient.innerHTML = email.sender;
  }
  mailDiv.append(recipient);

  const subject = document.createElement('div');
  subject.id = "email-subject";
  subject.className = "col-lg-6 col-md-5 col-sm-12";
  subject.innerHTML = email.subject;
  mailDiv.append(subject);

  const timestamp = document.createElement('div');
  timestamp.id = "email-timestamp";
  timestamp.className = "col-lg-3 col-md-3 col-sm-12";
  timestamp.innerHTML = email.timestamp;
  mailDiv.append(timestamp);

  // Check which mailbox the user is in and display the correct button text for archiving
  console.log(mailbox);
  if (mailbox === "inbox") {
    const button = document.createElement('button');
    button.id = "archive-button";
    button.innerHTML = "Archive";
    mailDiv.append(button);
    button.addEventListener('click', () => change_mail_archive(email.id, email.archived) );
  }
  if (mailbox === "archive") {
    const button = document.createElement('button');
    button.id = "archive-button";
    button.innerHTML = "Undo";
    mailDiv.append(button);
    button.addEventListener('click', () => change_mail_archive(email.id, email.archived) );
  }

  recipient.addEventListener('click', () => view_email(email.id) );
  subject.addEventListener('click', () => view_email(email.id) );
  timestamp.addEventListener('click', () => view_email(email.id) );
}

function change_mail_archive(email_id, previousValue) {
  // function takes in the email.archived value and just changes it to the opposite
  const newValue = !previousValue;
  console.log(`update: email is now ${newValue}`);
  fetch(`/emails/${email_id}` , {
    method: 'PUT',
    body: body = JSON.stringify({
      archived: newValue
    })
  })
  load_mailbox('inbox');
  window.location.reload();
}

function view_email(email_id) {
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {

    email_is_read(email.id);
    console.log(email);

    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#emails-specific').style.display = 'block';

    const view = document.querySelector('#emails-specific');
    const reply = document.createElement('button');
    reply.className ="btn btn-primary";
    reply.innerHTML = "Reply";

    document.getElementById('reply-button').onclick = function() {
      compose_email();

      document.querySelector('#compose-recipients').value = email.sender;
      if(email.subject.indexOf("Re: ") === -1) {
        email.subject = "Re: " +email.subject;
      }
      document.querySelector('#compose-subject').value = email.subject;
      document.querySelector('#compose-body').value = `\n\nOn ${email.timestamp} ${email.sender} wrote: \n\n${email.body}`; 
    };

    

    document.querySelector('#email-specific-sender').innerHTML = email.sender;
    document.querySelector('#email-specific-recipient').innerHTML = email.recipients;
    document.querySelector('#email-specific-subject').innerHTML = email.subject;
    document.querySelector('#email-specific-date').innerHTML = email.timestamp;
    document.querySelector('#email-specific-body').innerHTML = email.body;
    
    });

  return false;

}

function email_is_read(email_id) {
  // Call the API to change the read attribute from false to true
  fetch(`/emails/${email_id}` , {
    method: 'PUT',
    body: body = JSON.stringify({
      read: true
    })
  });
}

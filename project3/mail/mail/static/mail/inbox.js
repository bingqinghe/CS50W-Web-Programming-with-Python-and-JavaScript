document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-body').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-body').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(mailbox);
    console.log(emails);
    emails.forEach(element => {
      console.log(element);
      if(mailbox == 'inbox') {
        if(element.read) {
          class_read = 'read';
        } else {
          class_read = '';
        }
      } else {
        class_read = '';
      }
      if(mailbox == 'sent') {
        recipients = element.recipients;
        title = 'To: ';
      } else {
        recipients = element.sender;
        title = '';
      }

      var item = document.createElement('div');
      item.className = `card border-primary text-dark ${class_read} cardmargin`;
      item.innerHTML = `<div class='card-body'><b>${title}</b><b>${recipients}</b> &nbsp | &nbsp <b>Sub: </b> ${element.subject} &nbsp | &nbsp ${element.timestamp} </div>`;
      document.querySelector('#emails-view').appendChild(item);
      item.addEventListener('click', () => open_mail(element.id, mailbox));
    })
  })
}

function open_mail(id, mailbox) {
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-body').style.display = 'block';
    document.querySelector('#email-content').innerHTML = 
    `<b>FROM: </b> ${email.sender}<br>
    <b>TO: </b> ${email.recipients}<br>
    <b>SUBJECT: </b> ${email.subject}<br>
    TIME: ${email.timestamp}<br>
    <div id='reply-btn'></div>
    <hr>${email.body}<hr>
    <div id='archive-btn'></div>
    </div>
    `
    if(mailbox == 'sent') return;

    let archive = document.createElement('button');
    archive.className = 'btn btn-warning';
    if(email.archived)  archive.textContent = 'Unarchive';
    else archive.textContent = 'Archive';
    archive.addEventListener('click', () => switch_archive(email.id, email.archived));
    document.querySelector('#archive-btn').append(archive);

    let reply = document.createElement('button');
    reply.className = 'btn btn-success';
    reply.textContent = 'Reply';
    reply.addEventListener('click', () => replyemail(email.sender, email.subject, email.body, email.timestamp))
    document.querySelector('#reply-btn').append(reply);

    readmail(email.id)
  })
}

function switch_archive(id, value) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !value
    })
  })
  window.location.reload();
}

function replyemail(sender, subject, body, time) {
  compose_email();
  if(subject.slice(0, 4) != 'Re: ' ){
    subject = `Re: ${subject}`;
  }
  document.querySelector('#compose-recipients').value = `${sender}`;
  document.querySelector('#compose-subject').value = `${subject}`;
  document.querySelector('#compose-body').value = `Original: ${sender} wrote:\n\n${body}\n\nOn: ${time}\n-------------------------------------------------`;
}

function readmail(id) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
}
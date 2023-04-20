document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document.querySelector("#inbox").addEventListener("click", () => load_mailbox("inbox"));
  document.querySelector("#sent").addEventListener("click", () => load_mailbox("sent"));
  document.querySelector("#archived").addEventListener("click", () => load_mailbox("archive"));
  document.querySelector("#compose").addEventListener("click", compose_email);

  // By default, load the inbox
  load_mailbox("inbox");

  // Event listeners
  document.querySelector("#compose-form").addEventListener("submit", (e) => {
    e.preventDefault();
    recipients = document.querySelector("#compose-recipients").value;
    subject = document.querySelector("#compose-subject").value;
    body = document.querySelector("#compose-body").value;
    send_email(recipients, subject, body);
  });
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#compose-view").style.display = "block";
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#email-view").style.display = "none";

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#email-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "none";

  // Show the mailbox name
  document.querySelector("#emails-view").innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;

  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      emails.forEach((email) => {
        formatted_email = create_email_element(email);

        if (email.read) {
          formatted_email.style.backgroundColor = "grey";
        }

        document.querySelector("#emails-view").append(formatted_email);
      });
    })
    .catch((error) => {
      console.error("Fetch error:", error);
    });
}

function show_email(id) {
  document.querySelector("#email-view").style.display = "block";
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "none";

  // Clear old email view
  document.querySelector("#email-view").innerHTML = "";

  fetch(`/emails/${id}`)
    .then((response) => response.json())
    .then((email) => {
      const email_view = document.createElement("div");
      const sender = document.createElement("h3");
      const subject = document.createElement("h1");
      const timestamp = document.createElement("h3");
      const body = document.createElement("p");

      subject.textContent = email.subject;
      sender.textContent = email.sender;
      timestamp.textContent = email.timestamp;
      body.textContent = email.body;

      email_view.append(subject, sender, timestamp, body);
      document.querySelector("#email-view").append(email_view);
      mark_as_read(id);
    });
}

function mark_as_read(id) {
  fetch(`/emails/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      read: true,
    }),
  });
}

function send_email(recipients, subject, body) {
  fetch("/emails", {
    method: "POST",
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body,
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      // Print result
      console.log(result);
    });
}

// Generates email element to append to mailbox view
function create_email_element(email) {
  const email_div = document.createElement("div");
  const subject = document.createElement("h2");
  const sender = document.createElement("h4");
  const timestamp = document.createElement("h6");

  email_div.classList.add("email-entry");
  subject.classList.add("email-subject");
  sender.classList.add("email-sender");
  timestamp.classList.add("email-timestamp");

  subject.textContent = email.subject;
  sender.textContent = email.sender;
  timestamp.textContent = email.timestamp;

  email_div.append(subject);
  email_div.append(sender);
  email_div.append(timestamp);

  email_div.addEventListener("click", () => {
    show_email(email.id);
  });

  return email_div;
}

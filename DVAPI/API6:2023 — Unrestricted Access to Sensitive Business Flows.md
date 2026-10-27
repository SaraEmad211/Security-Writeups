## Challenge 6 — API6:2023 — Unrestricted Access to Sensitive Business Flows

**Challenge Idea:** Use Burp Suite Intruder with null payloads to repeatedly submit support-ticket requests and investigate whether the ticket-submission flow can be abused to trigger unintended behavior.

**Root Cause:** The ticket-submission flow relies on a ticket-count check before creating a new ticket. The controller's handling of this check and its failure path can lead to unintended behavior when requests are repeated.

**Vulnerable Code**
```javascript
const ticketId = generateId();

checkTicket(ticketId)
  .then(() => {
    const ticket = new Ticket({
      ticketId: ticketId,
      message: message,
      new: true
    });

    ticket.save().then(() => {
      res.send({
        status: "success",
        Message: "Ticket Created your ticketId is :" + ticketId
      });
    });
  })
  .catch((err) => {
    // The challenge flag is returned here.
  });
```

**Fixed Code (Illustrative):**
```javascript
const MAX_TICKETS = 150;

const ticketCount = await Ticket.countDocuments({});

if (ticketCount >= MAX_TICKETS) {
  return res.status(429).json({
    status: "error",
    message: "Ticket limit reached"
  });
}

// Validate the request and create the ticket only
// after the business rules have been enforced.
```

**Fix:** Validate ticket-submission rules explicitly, handle errors separately from expected business outcomes, and apply appropriate rate limits and business-flow controls to prevent automated abuse.

**Key Takeaway:** Sensitive business flows need controls that prevent automated requests from bypassing intended business rules or triggering unintended outcomes.

# Genuine demonstration: target 58 seconds, hard limit 60

## Before recording

Complete real MySQL testing first. Do not record the mock server as evidence of persistence. Start normal `backend/app.py`, load safe demo records, and run the Postman collection against that server. Keep its actual 404 and 400 results ready.

Arrange three windows: VS Code (running Flask terminal), browser, Postman. Have routes and schema open in editor tabs and GitHub history available for instructor questions. The one-minute video focuses on the operations required by section 7 of the assignment.

Use two browser tabs: A shows the list; B has a fully filled, **unsent** New Opportunity form. Prepare B before recording so nine fields do not have to be typed in ten seconds. Example: SDN Flow Optimization; Compare routing strategies.; Computer Networks; Demo Faculty; Computer Science; Python, Mininet; 3; 2026-12-25; Open. Do not submit until the recording reaches Create. Rehearse the window switches and keep the mouse near the next control.

## Timeline and spoken script

| Time | Action | Say |
|---|---|---|
| 0:00–0:06 | Show Flask terminal | “I’m Sohrab, 24P-0604. This is my research portal’s Flask server.” |
| 0:06–0:12 | Show list in tab A; Refresh | “The frontend retrieves research opportunities through the REST API.” |
| 0:12–0:22 | Switch to prepared tab B; show fields; click Create | “I submit this prepared form to create an opportunity.” |
| 0:22–0:30 | View new row; show all details | “View retrieves the complete record using its unique ID.” |
| 0:30–0:38 | Edit; change positions to 5; Save Changes | “I update the available positions and save.” |
| 0:38–0:44 | Close new row | “Close changes its status from Open to Closed.” |
| 0:44–0:50 | Delete the demo row; confirm | “Delete removes the selected test opportunity.” |
| 0:50–0:56 | Postman: show actual deleted-ID GET and 404 | “This deleted-ID request returns 404 Not Found.” |
| 0:56–0:58 | Show actual POST request and 201 response | “Postman also verifies creation. Thank you.” |

The Postman deleted-ID example may be the record deleted during the collection run; state that clearly if asked. Do not imply it is the browser record unless you actually send that ID. End by 58 seconds to allow a margin. Retake if any action stalls; never fabricate responses.

## Recording and delivery

Use your installed screen recorder, select the application area, test microphone/audio, rehearse once with a stopwatch, and then record the real actions. Preview the complete exported video and confirm duration is at most 60 seconds. Put the genuine MP4 into the final ZIP or write its accessible link in `VIDEO_LINK.txt`. Verify the link without your own signed-in account. No recording or video link was created during this audit.

The original `DEMO_AND_VIDEO_SCRIPT.docx` is preserved. Use this shorter script and current test report instead of its historical claims that MySQL/Postman tests already passed.

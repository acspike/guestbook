#!/bin/bash

rclone copy /opt/guestbook/messages guestbook:/GuestbookMessages \
  --log-level INFO \
  --log-file "/opt/guestbook/logs/rclone_sync.log"
LiSpeak - English Only Beta Preview
=======

A voice command system built on the base of Palaver

How to Install
======
1. Download and extract LiSpeak (we recommend your home folder)

2. Run ./lispeak --setup          (you can use --debug to see whats happening "behind the scenes")

3. Configure a keyboard shortcut for ./hotkey - We recommend setting the hotkey command to something like "bash /home/USER/LiSpeak/hotkey" as this seems to work best. "bash" folled by the complete path.

NOTE: Ubuntu 13.10 users will need to log out and back in after setting a shortcut. 

4. That's it!

Language Support
======
Altough this is the English only preview, we always could use a hand translating LiSpeak. If you have any questions about translating, read the wiki or submit and issue with the tag "translations"

Window Focus
=======
Plugins can add dictionaires that are applied only when a certain window is in focus.

The gedit control plugin is only in effect while gedit has focus.

Services
======
Services are plugins that run in the background and provided non-command features.

Services will also have access to the LiSpeak app indicator to add addition toggles and commands. (This is still under development)

Example:
    The Android plugin is a service, it doesn't add any commands but creates a service that uses http protocol to allow mobile phones to send it commands.
    
Multi-User Support
=======
The way plugins are installed was modified so their is now much better multi-user support. One user's plugins will no longer interfere with another user's.

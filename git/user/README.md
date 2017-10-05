# Fetch Other Websites Account via Git Account
The script get_info_git.py is used for dumping the developers' name, login, company, location and e-mail.
The script get_info_stackoverflow.py is used for dumping the developers' display_name, location and github account.
The script name_form.py lists the possible Stack Overflow display_name for a developer found in the github commit history.
Run the script main.py and you can get a json file containing developers' info of github and Stack Overflow display_name.

It is easy to get the info of developers in the github commit history using github API. However, it's complicated to get the corresponding info of the same user on Stack Overflow since the info for mapping is limited. Only the username and location of a developer can be obtained, which means we should list different possible usernames for each user in the commit history. Possible name forms need to be found, and the range of related users can only be narrowed by info of location now, which is insufficient.

Fortunately, the relating github account has been found in the Stack Overflow users' profile, which, however, is not accessible through Stack Overflow API but can be extracted from the source code of the users' profile page, of which the url is something like:

https://stackoverflow.com/users/user_id

That is to say, we can get the github account using user_id. For the possible username of developers on Stack Overflow, the user_id can be obtained through API. And then the github account can be extracted from the source code of the web page using Regular Expression.

However, few users have been found to provide their github account on their profile page, which makes the mapping between developers on github and stack overflow hard to finish.

The next step is to establish the possible username list using a generally form which can be used for all users.

Author: AlvinZSJ

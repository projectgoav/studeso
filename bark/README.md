<h1> studeso <small> Bark</small></h1>

<p>The code powering Bark Website</p>

<h2>Requirements</h2>
<ul>
	<li> Django 1.7 <i>In requiremnets.txt</i> </li>
	<li> Django-Bootstrap3 <i>In requirements.txt</i> </li>
	<li> Pillow <i>In requirements.txt</i></li>
	<li> Bootstrap CSS 3 <i>(provided)</i> </li>
	<li> Bootstro <i>(provided)</i></li>
	<li> Taggle <i>(provided)</i></li>
</ul>

<h2>Installation</h2>

<p>Clone repo from git:<br><code>git clone https://github.com/projectgoav/studeso</code></p>

<p><i>Optional</i> - Create a virtual environment </p>

<p>Install requirements with provided pip requirements file<br><code>pip install requirements/requirements.txt</code></p>

<p>After installing with pip, navigate to the Bark directory. </p>

<p>Create and setup the database. <br><code>python manage.py syncdb</code><br><br>Create a superuser account, if you so wish.</p>

<p>Fill the database with some sample data and user accounts.<br><code>python populate.py</br></p>

<p>Before running the server, navigate to the second Bark directory. You should see a lot of python files and 2 folders named <b>management</b> and <b>templatetags</b>. Create <b>keys.py</b> file here and enter this information:<br><code>USERNAME=''<br>Password=''</code><br><i>This allows bark to send email. You can put in your own email details here if you wish to test the email functions. <br><b>Note</b>If you are using a provider other than Outlook, you'll need to change the EMAIL_HOST and EMAIL_PORT settings in bark.settings.py.<br>If you leave the USERNAME and PASSWORD blank Bark will still work. It is not required</i></p>

<p>You're not ready to roll! Run the Django development server <br><code>python manage.py runserver</code></p>

<h2>Test User Logins</h2>
<ul>
	<li> <b>Username</b> | <b>Password</b> </li>
	<li> ghastly | Test </li>
	<li> stuck_student55 | Test </li>
</ul>

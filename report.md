##Experiential learning
####Student: Guinsly Mondésir
####Ottawa University

###Resume
I had a great experience while doing this Experiential Learning. I learned a lot about servers and what tools to use to monitor the performance of a server. The Lagotto project is quite **ambitious** and I really like their vison. They are providing a metrics services with a large scope of information retrieval in differents sources  (i.e. Twitter, wikipedia, Reddit etc.). It's a [Scopus](http://www.scopus.com/) or a [SemanticScolar](https://www.semanticscholar.org/) but wider. My reflection was that publishers need a a server in order to post their contents (scholarly articles) or will require a service like Lagotto for their server. Meaning that a publisher could require the Lagotto web application to provide more functionnality and help the user to evaluate efficiently the different impact that a paper have in the internet. I provide below a details documentation of what I accomplished. In regards of the objectives of fidings way or solution to resolve the downtime issues of the server, I was incapable to solve that issues. I took many approaches. First I analysed the **production.log** file to correct any errors found, then I analysed into **sidekiq.log** to found issue due to failed background jobs, then I looked into **redis**, then I added a **swapfile** of 4GB. But none of this approached couldn't point out the root causes analysis of the downtime issues that the server face sometimes. 

##1 What was my mission

objective (Dr. Morrison)
<ul>
	<li> 30 hours work is the expected maximum</li>
	<li> time frame: completion by end of Nov. 2015 (some flexibility to extend)</li>
	<li> deliverable to be determined by the two of you based on project selection</li>
	<li> 1-page paper summarizing the project to be submitted to myself for marking purposes</li>
	<li>  	 marking: pass / fail based on confirmation by supervisor (Dr. Felczak) of completion </li>
</ul>

##1.1 Project : Lagotto

[http://pkp-alm.lib.sfu.ca/](http://pkp-alm.lib.sfu.ca/) <br>
    [http://lagotto.io/](http://lagotto.io)<br/>
    [https://github.com/lagotto/lagotto](https://github.com/lagotto/lagotto)
    
**Date start working on the project**: +-November 1st <br/>
**Date to start Experiential Learning**: November 1st <br />
**Date finish**: +-November 28th

####1.1.2 Project objective

This project objective is the latest one that I receive before starting the project.
[Notes 10. Dr. Alperin]

<ol>
<li>The server itself has been going down (giving a 502 error). Doing a diagnostic of the server (figuring out what might have failed, what we might be able to do to fix it) would be extremely useful. 
</li>
<li>From within the app, the different "sources" also generate a bunch of "alerts" that can be viewed once logged in (these can also be seen directly in the DB). Looking into each of the sources and figuring out a) if they are collecting data regularly; b) if they are getting data for all articles; and c) if there is any configuration we can fix would be useful. 
</li>
<li>More generally, anything that you can do to give us a better idea of what is happening on the server with regards to the app would be helpful. We are running it a little blind, because it uses technologies we are not familiar with, and so documentation or tips on how to look in on the app (i.e., what to look for, where to look, to make sure things are running as expected) would help us. </li>
</ol>

####1.1.3 [Communication] The persons who I communicate with or the ressource that I uses
    1.Pkp
        *Michael Felczak (Pkp-Supervisor)
        *Juan Pablo Alperin (Lagotto-Supervisor)
        *Jason Nugen (ssh issue)
    2.Other resources use
        *Stackoverflow
        *IRC #redis channel

##What did I do (detailed documentation)


I officially started to work on the server by Oct 29. Because it was by that time that I could login to the server **notes 1**. But previously, by Nov 21st, due that my supervisor told me that the server had some downtime I added an entry on [uptimerobot](https://uptimerobot.com/) so that I could check the frequency of the downtimes. So between those 2 dates we had only 1 downtime which was on Nov 29th [**notes 2**].  


So the same day (Nov 29th) I had to delete the **sidekiq.log** file. My  supervisor told me to take a look at it and delete the lines that are unrelevant [**notes 3**]. But I couldn't do so because the server were almost out of disk space. Only a few ko left when I logged in. Meaning that the file **sidekiq.log** took pretty much the 34Gb space left on the disk. I as I couldn't **cat** the file because there were no space left on the disk And as I couldn't download the file (via sftp) because it was taken too much time. I decided to delete the file that same day because after a few hours the server would have shut down anyway due to the lack of space left to register logs.

The following week I started to try to solve the issue that Dr Alperin told me about the **docs** [notes 4]. Meaning that on the **production.log** file there were (and still are) an error showing up that keep repeating several times in a day.
```ruby
{"message":"  Couldn't find template for digesting: docs/#{@doc.layout}","@timestamp":"2015-10-28T22:15:05.963+00:00","@version":"1","severity":"ERROR","host":"pkp-alm.lib.sfu.ca"}
```

As the error stated, I was sure that there were a template file missing. Even though my objectives was to work on the server as stated by Dr. Alperin. I downloaded the application to my local machine. But when I run the application on development I didn't have this issue on my **development.log** file. So I logged in back to the server to debuged the **@doc** variable. I found that there were a **partial** file missing [**notes 5**]. One of this Model field called **layout** **[notes 6 gist]**(https://gist.github.com/guinslym/f8fa80efc56c5c350fe7). But even though I create manually some dumb file to mimic the **_home.html.erb** file missing I still had the same issue on the server log **production.log**. So I almost gave up only to find out there were a Rails' Github issue open about that. **[notes 7]** see last comment](https://github.com/rails/rails/issues/15255#issuecomment-155953924). Notes that this Github issue is stated as Closed but as other users still experienced the same issue that why I say that it's open meaning that there were no solution provided on the Rails documentation. So I finally gave up on that issue.


The other issue that I noticed was due to a mysql statement. 
```python
{"message":"Mysql2::Error: Incorrect string value: '\\xF0\\x95\\x94\\xA3P\u003c...' for column 'title' at row 1: UPDATE `works` SET `title` = 'Extraction du complexe (𕔣P\u003csub\u003e2\u003c/sub\u003eW\u003csub\u003e17\u003c/sub\u003eO\u003csub\u003e61\u003c/sub\u003eFe)7-, par membrane liquide emulsionnee', `updated_at` = '2015-10-29 01:32:19' WHERE `works`.`id` = 99484","@timestamp":"2015-10-29T01:32:19.632+00:00","@version":"1","severity":"ERROR","host":"pkp-alm.lib.sfu.ca","tags":["ActiveJob","SourceJob","18a64e63-5b78-4f78-9c6a-427d444d66f8"]}
{"message":"Mysql2::Error: Incorrect string value: '\\xF0\\x95\\x94\\xA3P\u003c...' for column 'message' at row 1: INSERT INTO `alerts` (`message`, `class_name`, `source_id`, `created_at`, `updated_at`, `hostname`, `trace`) VALUES ('Mysql2::Error: Incorrect string value: \\'\\\\xF0\\\\x95\\\\x94\\\\xA3P\u003c...\\' for column \\'title\\' at row 1: UPDATE `works` SET `title` = \\'Extraction du complexe (𕔣P\u003csub\u003e2\u003c/sub\u003eW\u003csub\u003e17\u003c/sub\u003eO\u003csub\u003e61\u003c/sub\u003eFe)7-, par membrane liquide emulsionnee\\', `updated_at` = \\'2015-10-29 01:32:19\\' WHERE `works`.`id` = 99484', 'ActiveRecord::StatementInvalid', 12, '2015-10-29 01:34:26', '2015-10-29 01:34:26', 'ip-172-31-6-118.ec2.internal', '/app/models/work.rb:153:in `get_ids\\'\\n/app/models/sources/pmc_europe_data.rb:6:in `get_query_url\\'\\n/app/models/source.rb:159:in `get_data\\'\\n/app/models/retrieval_status.rb:42:in `perform_get_data\\'\\n/app/jobs/source_job.rb:43:in `block (2 levels) in perform\\'\\n/app/jobs/source_job.rb:42:in `block in perform\\'\\n/app/jobs/source_job.rb:30:in `each\\'\\n/app/jobs/source_job.rb:30:in `perform\\'')","@timestamp":"2015-10-29T01:34:26.357+00:00","@version":"1","severity":"ERROR","host":"pkp-alm.lib.sfu.ca"}
```

I finally ran a **rake db:seed** that will find the proper Work model and correct the title to __Extraction du complexe__ I don't have a direct access to mysql (I don't have the password) so I had to find another way to make the changes into the db.


Then the **production.log** file were ok with me. I still had these errors
```ruby
{"message":"  Couldn't find template for digesting: docs/#{@doc.layout}","@timestamp":"2015-10-29T00:59:27.708+00:00","@version":"1","severity":"ERROR","host":"pkp-alm.lib.sfu.ca"}
```
But I didn't mind because there is nothing that I can do right now. So the production file looks ok for me but **we still have some downtime**. So I was pretty sure that the downtime were not causes by the application itself so I took another approach


The following weeks I looked into Sidekiq.log. I stayed about two weeks mainly is because that I didn't know sidekiq enough to make a modification on the server. So I had to read the sidekiq documentation. I had this issue on the **Sidekiq.log** file:

```ssh
2015-11-10T03:07:39.602Z 21565 TID-16b40s ERROR: heartbeat: EXECABORT Transaction discarded because of previous errors.
```

I finally had some guidance to solve an Sidekiq issue. I create an SO question [**notes Stackoverflow**](https://stackoverflow.com/questions/33623027/what-is-the-causes-of-exhausted-2-retries-in-sidekiq-log). So this was an Redis issue so I increased the maximum memory of Redis. But the problem still remains **the downtimes still occurs**. So I went directly on the Redis IRC channel to have some guidance because I thought that **Redis** was the problem for the downtimes. What I had as clue from the, irc conversation, to solve the **EXECABORT** issue didn't resolve it nor correct the downtime issue of the server. **notes ** irc log (http://irclogger.com/.redis/2015-11-13) user: gmond071. 


Whithin those 2 weeks of learning sidekiq I also logged in a lot on the server to watch the RAM (memory) usage and to find which processes used the most memory. I found out that sometimes there is 2Gb RAM left and sometimes there is about 73MB left on memory usage. What's that means is that sometimes the background jobs of the Rails application (cron + sidekiq) use almost all the RAM left. But something were odds I had as an hypothesis that it was because that the server didn't have that much memory left (73mb) that's why it had some downtime. 


But one day I logged into via ssh to monitor the memory usage while the server had a downtime and I found out there is **no relation between the downtime and the memory usage**. Because while the server experienced a downtime there were almost 2 Gb of free space left of the memory (RAM). I installed [logentries](https://logentries.com/) so that I can monitor the website RAM usage. Because even though I was sure that the memory usage doesn't cause the downtime. I actually have no prove of that because I couldn't find a way to know the RAM usage before a downtime. I only logged into the server when I had downtime so that I could monitor the RAM usage **post** downtime but I have no idea of the RAM usage **pre** downtime. The free student plan I have with **Logentries** didn't monitor the RAM usage. In order to do so I had to installed the gem version in the Gemfile app. But my ssh account didn't allows me to install Gems. 


Also because of my memory error (**EXECABORT**) I create an **Swapfile** of 4GB following some guidance of another user that had the same issue. **notes** (http://stackoverflow.com/a/28482225/2581266). 


So neither of my approach: **production.log, sidekiq.log,  redis.conf** or monitor the RAM, worked to solve the server downtime issue. So now I turned to **passenger** itself because I realize that when the server experienced a downtime it's a **passenger** default html page that showed up. 

![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")

If it was the Rails application that had an error the error page would have been different. I couldn't investigate that approach because by Nov 19 I couldn't access to the server by ssh anymore. 


What happened? This was unclear. I receive about 3 email notification that the server experiencing a downtime. **Status: 503 Service Unavailable** This was quite odd to have all this downtime whithin maybe 3 hours so I logged in several time to monitor the RAM usage. Then all of a sudden I didn't have access anymore. When I went to **logentries** to check the **Auth.log** I noticed that the same day the authentification had some issues but I was still capable to connect via ssh. But by 5 pm I couldn't connect to the server anymore via ssh.

What happened next? or What I did next? I communicated the problem to Dr. Alperin which communicated it to Jason. 


#Conclusion

Unfortunately I still don't know why the server experience **downtimes**.
- I am wondering if we run a server on a local for let's say 24 hours if the server will experienced downtime. 
- Even though I say that there is no relation between the memory usage and the downtime I still don't like the idea that the memory usage is so unstable because of all the background jobs.
- For the sidekiq.log file issue. One of the issue that I didn't mentionned is that this file growth exponentially. Meaning that the file size increased too fast. On the cron jobs. I would have comment on Production the outputs except if there is an error
- Jason told me that the server had some downtimes because of the database server. I don't know much about that I couldn't investigate due to the ssh connection issue


I calculated that I did about 15 hours on the server by using the unix **last** command and computing only the connection that was access by the Ottawa University and my home router ip. Precisely I did 11.48 hours from Nov 3 to Nov 15. The **last** command has a default limit so I couldn't calculate my connection before Nov 3rd and between Nov 15 and Nov 19 (ssh issue) I didn't download the logs so that I could prove how exactly how many hours. But outside the server I did definetively more then the 15 hours reading docs and experiment (StackOverflow + IRC + dstat + downloading the error logs and analyse them + sidekiq + htop + redis + passenger + man ps + logentries + uptimerobot + rails meeetup (that where I found about logentries and an overview of Sidekiq) + testing an offline version of lagotto app)). 

This was a great experience like I stated before. What would I have changed? Even though I had good guidance from Dr Alperin and Dr Felzcak if I had to redo the experience I don't think I would have done it because this project requires more time than the 30 hours. I am pretty sure that I did my 30 whithin the first week. Causes I need to read the Lagotto code and understands it. Also with constant email notifications that I receive, several times during a day I had to stop what I am doing and logged into the server. What I mean by that is my colleages, they are working 5 to 8 hours straight, when I am doing an homework or when I  am in class I need to stop and go online and read the logs to find what causes the downtime. So I had a lot of distraction outside of my dedicated time to work on the server. Also my expertise is in programming (ruby or python). But this project was different is was like a system administrator related task. So I didn't had to program much, except to write some **sed**, or **shell** script. The **XMLP** project was more suited for me or for a student because I need to concentrate on application within a project (i.e. debugging the PDFconversion module) instead of the sys admin task that I had. Because the sys admin task require to look or try many directions (redis, application, passenger etc...) and within 30 hours it wasn't possible. And as an intership I tought I was going to work on the development side (source code) but I was working on Production. But the benefit of doing this Experiential Learning compare to my other colleagues is that I was to be autodidact, think outside of the box and try many solutions.
# bigrams and trigrams not working in gensim
# https://www.youtube.com/watch?v=TKjjlp5_r7o&list=PL2VXyKi-KpYttggRATQVmgFcQst3z6OlX&index=10


# import libraries
from fileinput import filename
import numpy as np
import json
import regex as re

import datetime
e = datetime.datetime.now()

import os
from os import path

# Spacy
import spacy
from spacy.symbols import nsubj, VERB
nlp = spacy.load("en_core_web_sm")

# VIS
# !pip install pyLDAvis
import pyLDAvis
import pyLDAvis.gensim_models

print ("The time is now: = %s:%s:%s" % (e.hour, e.minute, e.second))
os.chdir(r'C:\\Users\\bminn\\Documents\\PROJECT INVESTIGATION\\NLP\\ExtractJobPost\\')
print(os.getcwd())

# load json data
def load_json(filename):

    listObj = []

    # Check if file exists
    if path.isfile(filename) is False:
        raise Exception("File not found")
 
    # Read JSON file
    with open(filename) as fp:
        listObj = json.load(fp)
 
    print('Successfully loaded JSON file\n')        

    return listObj

# save json data
def write_data(file, data):
    with open (file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print('Successfully saved JSON file\n')   

# load specific key from file
savedJobs = load_json("SavedJobPosts - Copy - Copy.json")

# finding verbs, entities using defaut tools and head_text
for post_dict in savedJobs:
    # initialize sets
    verbs = set()
    ents = set()
    head_text = set()    

    doc = nlp(post_dict['spaCy_lemma_wo_stop'])

    if not 'verbs' in post_dict:
        for possible_subject in doc:
            if (possible_subject.dep == nsubj) and (possible_subject.head.pos == VERB):
                verbs.add(possible_subject.head.text)
        # update
        post_dict['verbs'] = json.dumps(list(verbs))

    if not 'ents' in post_dict:
        for ent in doc.ents:
            ents.add((ent.text, ent.label_))
        # update
        post_dict['ents'] = json.dumps(list(ents))

    if not 'head_text' in post_dict:
        for chunk in doc.noun_chunks:
            head_text.add(chunk.root.head.text)
        # update
        post_dict['head_text'] = json.dumps(list(head_text))

## now, to find our keywords
# read json patterns
patterns = load_json("LabeledPatterns.json")
# create new pipe
nlp = spacy.blank("en")
ruler = nlp.add_pipe("entity_ruler")
# iterate
for pattern in patterns:

    ruler.add_patterns(pattern)
    print(nlp.pipe_names)
    doc = nlp("About the job More than the opportunity of a lifetime the chance to improve lives Boston Scientific is one of the worlds largest medical device companies employing over employees. It develops manufactures and markets more than products in over countries treating approximately million patients annually. The medical devices are used in various interventional medical specialities including interventional cardiology peripheral interventions neuromodulation neurovascular intervention electrophysiology cardiac surgery vascular surgery endoscopy oncology urology and gynaecology. We are excited to add a new Machine Vision System Engineer to our Equipment Engineering Group here at our Galway site. As our successful candidate you will work with our manufacturing partners to develop new and innovative vision solutions in line with our Industry . Smart Factory strategies. Innovative vision solutions offer the opportunity to deliver intelligent manufacturing machines and optimise production systems while working in a purpose built technology innovation laboratory. You will also have the chance to assist R D and Operations on New Product Development Programs and Sustaining Programs by participating in the Prototyping Design Build Commissioning and Qualification of New Equipment as well as Equipment Upgrades. The role is primarily based in Galway a world class facility although travelling abroad may be required from time to time for short periods. Working times are usually Monday to Friday although some periodic weekend work may be needed per production schedules. Key Activities Of The Role Define implement and maintain architectures to retrieve archive and analyse production image data. Develop test validate and deploy computer vision systems using open source and proprietary tools such as VisionPro Insight and MVTech. Provide strong leadership and problem solving to enable equipment technology innovation. Work closely with the customer to understand product visual inspection requirements and propose creative and cost effective solutions to automate inspections. Generate quotations concepts and business cases for new and upgraded business systems. Ensure equipment and business requests are processed promptly and effectively and manage the execution of results. Determine project schedules and work with the team and other departments across the plant to ensure adherence. Manage projects and portions of projects as part of a larger team. Lead and participate in cross functional Design Reviews. Draft and Review Design and Compliance Quality System documentation. Write detailed functional design requirements. Contribute to all phases of software development including design implementation unit test integration release and validation support. Qualifications Experienced Engineering qualification equivalent to or above NFQ Level Three plus years of experience developing Vision Systems is essential. Proprietary Machine Vision Image Processing tools e.g. Cognex VisionPro and Insight MVTec LabVIEW . Optics sensors and lighting applied to industrial machine vision. C#.NETor similar. Digital Image Processing techniques and dataflows applied to industrial machine vision. Advance Statistical analysis knowledge. Proprietary Machine Learning software e.g. Cognex VIDi MVTec Matlab is preferred. Basic knowledge of deep learning theory and techniques is desirable. TensorFlow OpenCV and Pandas in Python environments are desirable. Knowledge of Robotics and Controls. GAMP Documentation life cycle for regulated industries Imaginative and creative approach to problem solving and continuous improvement. At Boston Scientific we recognise that nurturing a diverse and inclusive workplace helps us be more innovative. It is essential in advancing science for life and improving patient health. We stand for inclusion equality and opportunity for all. By embracing the richness of our unique backgrounds and perspectives we create a better more rewarding place for our employees to work and reflect the patients customers and communities we serve. Boston Scientific is proud to be an equal opportunity and affirmative action employer")
    print(ent.text, ent.label_)


write_data("SavedJobPosts - Copy - Copy.json", savedJobs)

# Finding a verb with a subject from below - good
## Removing the stop words yielded more results
## Results were similar to the above


# print noun chunks
## What I discovered is the ROOT HEAD TEXT lists key words which help finding their requirements
## Count and find the most frequent
## Finding the sentences where these words are used, can lead to extracting requirements.
'''
post = " ".join([token.lemma_ for token in doc if not token.is_stop])
print(post)
doc = nlp(post)
for chunk in doc.noun_chunks:
  print("TEXT^", chunk.text, "^ROOT TEXT^", chunk.root.text, "^ROOT DEP^", chunk.root.dep_, "^ROOT HEAD TEXT^", chunk.root.head.text)
'''

## the span trick does not really help... returns single words
'''
print("text", "^","pos_", "^","dep_", "^","head.text")
span = doc[doc[4].left_edge.i : doc[4].right_edge.i+1]
with doc.retokenize() as retokenizer:
  retokenizer.merge(span)
for token in doc:
  print(token.text, "^",token.pos_, "^",token.dep_, "^",token.head.text)
'''


print("\n")

## https://www.mckinsey.com/business-functions/mckinsey-digital/our-insights/the-top-trends-in-tech

## I would like to get an idea of the words' POS
## Supply Chain Key Words
'''
robotic 
automation
robotic automation
blockchain
logistics
channel operations
operations
'''
## Health Care Key Words

## Agriculture Key Words

## Applied AI Key Words
'''
3D Visuals
AI Applications
AI models
analyze huge sets
artificiall inteligence
augment capabilites
automate
automate activites
autonomous
better decisions
classification
computer vision
consumer
credit card fraud
customized recommendations
decision support
deep learning
deep reinforcement learning
derive insights
diagnosis-decision
discern patterns
forcasting
forecast demand
generate
generative AI models
increase efficiencies
knowledge graphs
machine learning (ML)
medical treatments
model
natural language processing
new drugs
optimization of operation
optimize
personalized
precise
precision
prediction
predictive
predictive tools
productivity forecasting
recognition
recomandations
recurring
reinforcement
software simulations
supervised
unsupervised
'''

## Connectivity Key Words. So these are like features. 
# the higher the frequency, the more interesting the job is. 
# Certainly, there shall be dublicate words between sectors
'''
5G
6G
AR
augmeneted reality
B2B
B2C
BIM
Building information modeling
cellular
cloud computing
cloud devices
cloud gaming
connected vehicles
connectivity
coverage
internet of things
IOT
latency
latency throughput
LEO
logistics
low power wide area
low-earth-orbit
LPWA
monitor
networks
nonterrestiral networks
NTN
sattelite
sattellites
selfdriving
smart grid
smart metering
smart mining
smart sensors
smart utility grid
spectrum
telecom
track and trace
virtual reality
VR
wireless low power
'''

## Bioengineering
'''
agriculture
biocomputing
biological
biology
biomachine
biomolecules
bioproducts
biosystems
cell
cellular
cultivate
cure
diseases
DNA
foodd
gene
gene therapies
genetic
health
healthcare
medical
monogenic
mutate
omics
organ
pharmaceuticals
polygenic
RNA
snthetic
therapy
tissue
viral vector
viruses
'''

## Mobility Key Words
'''
battery
blade
capacity
carbon
cell
charge
clean energy
decarbonization
demand
distribute
distribution
electric
electrification
emissions
energy
enironment
fossil
fuel
gas
generate
generation
green
grid
hydrogen
net zero
offshore
onshore
power
reliability
renewable
rotor
slectricity
smart
smart grid
solar
stability
storage
sustainable
turbine
utility
wind
'''

## Clean Energy Key Words
'''

'''

## General Key Words
'''
adopt
aid
algorithm
analyse
application
automation
benefit
better determine
capable
challange
complex
culture
contribute
cost effective
critical
confident
deliver
demand
deploy
derive
design
design process
detect
determine
develop
diagnose
digitize
downtime
degree
masters
PHD
efficient
electronics
enhance
enjoy
ethical
expand
explore
explore relationships
expert
expertise
generate
global
growth
identify
images
impact
improve
innovate
integrate
intensive
international
insight
global 
innovation
knowledge
learn
maximize
mechanisms
minimize
monitor
operations
optimize
potential
priority
plan
process
product
product development
progress
proud
passion
passionate
practical
recommend
regulatory
recognise pattern
pattern
remote
recognise
resolve
skill
service
service operations
solution
telecommunication
train
transform
unlock
videos
visual data
flexible hour
'''



## Applicable industries

'''
Aerospace and defense
Agriculture
Automotive and assembly
Aviation, travel, and logistics
Chemicals
Construction and building materials
Consumer packaged goods
Education
Electric power, natural gas, and utilities
Information technology and electronics
Media and entertainment
Metals and mining
Oil and gas
Pharmaceuticals and medical products
Public and social sectors
Real estate
Retail
Telecommunications
'''

## Extracted Skills from ENTS
'''
Adapt,SKILL
Adobe,SKILL
Adobe Experience Platform,SKILL
Advanced Analytics,SKILL
AI,SKILL
AI ML,SKILL
Airflow,SKILL
Algorithms,SKILL
Amazon Aurora,SKILL
Amazon Search,SKILL
Amazon Web Services,SKILL
Analytics,SKILL
Analytics Insights,SKILL
Apache,SKILL
Apache Airflow,SKILL
Apache Griffin,SKILL
Apache Kafka,SKILL
Apache Spark,SKILL
api,SKILL
Application Lifecycle Management,SKILL
Applied Scientists,SKILL
Architects,SKILL
Artificial Intelligence,SKILL
Athena,SKILL
AWS,SKILL
AWS Athena,SKILL
AWS Glue,SKILL
Azure,SKILL
Azure Data,SKILL
Azure Data Factory,SKILL
Azure Data Lake,SKILL
Azure Data Platform,SKILL
Azure Databricks,SKILL
Azure PowerShell,SKILL
Bash,SKILL
Beam,SKILL
BI,SKILL
BI Analytics,SKILL
Big Data,SKILL
BigQuery,SKILL
Cassandra,SKILL
Classification Text,SKILL
ClickHouse,SKILL
Cloud Azure,SKILL
Cloud Storage,SKILL
Cognex VisionPro,SKILL
Collaborate,SKILL
Computational Linguistics,SKILL
Computer Science,SKILL
Computer Vision,SKILL
Consumer Data,SKILL
Consumer Goods,SKILL
Container,SKILL
CRM,SKILL
CSS,SKILL
Customer Journey,SKILL
Cybersecurity,SKILL
Data Acquisition,SKILL
Data Analytics,SKILL
Data Architects,SKILL
Data Devops,SKILL
Data Engineer,SKILL
Data Engineering,SKILL
Data Engineers,SKILL
Data Governance,SKILL
Data Lake,SKILL
Data Modeler,SKILL
Data Modeling,SKILL
Data Modeller,SKILL
Data Platform,SKILL
Data Products,SKILL
Data Protection,SKILL
Data Science,SKILL
Data Scientist,SKILL
Data Scientists,SKILL
Data Visualisation,SKILL
Data Warehouse,SKILL
Data Warehousing,SKILL
Databrick,SKILL
Databricks,SKILL
DAX,SKILL
DataOps,SKILL
Degree Bachelors,SKILL
Deep Learning,SKILL
Deequ,SKILL
Developer,SKILL
DevOps,SKILL
Digital Research Intelligence,SKILL
Digital Science Innovation,SKILL
DL,SKILL
Docker,SKILL
Dockers,SKILL
DSI,SKILL
Econometrics,SKILL
ElasticSearch,SKILL
Electrical Engineering,SKILL
Electronics,SKILL
ELT,SKILL
Engineering Automation,SKILL
ERP,SKILL
Flink,SKILL
Gensim,SKILL
Git,SKILL
Github,SKILL
Gitlab,SKILL
Glue,SKILL
Golang,SKILL
Google,SKILL
Google Analytics,SKILL
Google Big Query,SKILL
Google Cloud,SKILL
GraphQL,SKILL
Hadoop,SKILL
Health,SKILL
Healthcare,SKILL
Hive,SKILL
IBM,SKILL
Informatica,SKILL
Information Technology,SKILL
Infrastructure,SKILL
Infrastructure Management,SKILL
Innovation Technology,SKILL
IoT,SKILL
Java,SKILL
JavaScript,SKILL
Jenkins,SKILL
Jira,SKILL
JVM,SKILL
K Means,SKILL
Kafka,SKILL
Kanban,SKILL
Keras,SKILL
K-Means,SKILL
Kraken,SKILL
Kubernetes,SKILL
Life Science,SKILL
Looker,SKILL
Machine Learning,SKILL
Machine Learning Automation,SKILL
Machine Learning Engineer,SKILL
MapReduce,SKILL
Marketing,SKILL
Masters Degree,SKILL
MastersDegree,SKILL
Mathematics,SKILL
Matlab,SKILL
Microsoft,SKILL
Microsoft Azure,SKILL
Microsoft Azure Certifications,SKILL
Microsoft Office Dynamics,SKILL
Microsofts Purview,SKILL
ML,SKILL
ML Engineering,SKILL
Mlib,SKILL
MLOps,SKILL
MS,SKILL
MS Azure,SKILL
MVP,SKILL
MVTec,SKILL
MVTech,SKILL
Natural Language,SKILL
Natural Language Processing,SKILL
NLP,SKILL
NLP AI,SKILL
NLU,SKILL
NoSQl,SKILL
Oracle,SKILL
Orchestration,SKILL
Pandas,SKILL
SKLearn,SKILL
Physics,SKILL
PostgreSQL,SKILL
Power BI,SKILL
Power Platform,SKILL
Presto,SKILL
Process Mining,SKILL
Programming Interfaces,SKILL
Project Service Management,SKILL
Purview,SKILL
Python,SKILL
PyTorch,SKILL
Qlik,SKILL
Qlikview,SKILL
Query M,SKILL
QuickSight,SKILL
Random Forest,SKILL
RDS,SKILL
Redis,SKILL
Redshift,SKILL
ReGex,SKILL
regular expressions,SKILL
Reinforcement Learning,SKILL
Reporting Analytics,SKILL
Research Analysts,SKILL
Research Development,SKILL
Retail,SKILL
Ruby,SKILL
SageMaker,SKILL
Sales,SKILL
SAP,SKILL
SAS,SKILL
Scala,SKILL
Scrum,SKILL
Shellscript,SKILL
SKLearn,SKILL
Snowflake,SKILL
Snowplow,SKILL
Software Developer,SKILL
Software Engineering,SKILL
Software Programming,SKILL
Solr,SKILL
Spark,SKILL
Spark Airflow,SKILL
Specialist Artificial Intelligence,SKILL
Spectrum,SKILL
Spring,SKILL
SQL,SKILL
SQL Azure,SKILL
SQL Query Optimization,SKILL
Statistics,SKILL
Storm,SKILL
Supply Chain,SKILL
Synapse,SKILL
Tableau,SKILL
Talend,SKILL
Tensorflow,SKILL
Teradata,SKILL
Terraform,SKILL
Text Classification,SKILL
Text Mining,SKILL
Textual Data Sets,SKILL
Theano,SKILL
web Analytics,SKILL
WhereScape,SKILL
'''

## Most Common Interview Questions
'''
What are your strengths?
What are your weaknesses?
Why are you interested in working for [insert company name here]?
Where do you see yourself in five years? Ten years?
Why do you want to leave your current company?
Why was there a gap in your employment between [insert date] and [insert date]?
What can you offer us that someone else can not?
What are three things your former manager would like you to improve on?
Are you willing to relocate?
Are you willing to travel? *(Post COVID-19)
Tell me about an accomplishment you are most proud of.
Tell me about a time you made a mistake.
What is your dream job?
How did you hear about this position?
What would you look to accomplish in the first 30 days/60 days/90 days on the job?
Discuss your resume.
Discuss your educational background.
Describe yourself.
Tell me how you handled a difficult situation.
Why should we hire you?
Why are you looking for a new job?
Would you work holidays/weekends?
How would you deal with an angry or irate customer?
What are your salary requirements? (Hint: if you’re not sure what constitutes a fair salary range and compensation package, research the job title and/or company on Glassdoor.)
Give a time when you went above and beyond the requirements for a project.
Who are our competitors?
What was your biggest failure?
What motivates you?
What’s your availability?
Who’s your mentor?
Tell me about a time when you disagreed with your boss.
How do you handle pressure?
What is the name of our CEO?
What are your career goals?
What gets you up in the morning?
What would your direct reports say about you?
What were your bosses’ strengths/weaknesses?
If I called your boss right now and asked him/her what is an area that you could improve on, what would he/she say?
Are you a leader or a follower?
What was the last book you read for fun?
What are your co-worker pet peeves?
What are your hobbies?
What is your favorite website?
What makes you uncomfortable?
What are some of your leadership experiences / What is your leadership style?
How would you fire someone?
What do you like the most and least about working in this industry?
Would you work 40+ hours a week?
What questions haven’t I asked you?
What questions do you have for me?
'''

'''
Good culture

Sweden^Sweden
Sweden^Specsavers            
Sweden^Centiro            
Sweden^Hilti            
Sweden^CAG            
Sweden^SBAB            
Sweden^Sparbanken Skåne AB            
Sweden^Sopra Steria            
Sweden^Three            
Sweden^Tyrann's            
Sweden^DHL Express            
Sweden^MTA Building and Construction            
Sweden^Erik Olsson Property brokerage            
Sweden^Synoptik Sweden AB            
Sweden^Bavaria Sweden Bil AB            
Sweden^Liseberg AB            
Sweden^WH Companies             
Sweden^Sign max            
Sweden^Key Solutions AB            
Sweden^Elvenite            
Sweden^Multisoft AB            
Sweden^AB Stångåstaden            
Sweden^Castra Group AB            
Sweden^PlantVision            
Sweden^Transcendent Group            
Sweden^RSM Sweden            
Sweden^Project Hagastaden, Exploateringskontoret, City of Stockholm            
Sweden^AbbVie            
Sweden^Tenant &amp; Partner            
Sweden^Hilton            
Sweden^Striking            
Sweden^Wihlborgs Fastigheter AB            
Sweden^Picadeli AB            
Sweden^Sentor MSS AB            
Sweden^Navigation            
Sweden^Chiesi Pharma AB            
Sweden^Fabege            
Sweden^OilQuick            
Sweden^The property owners MittNord AB            
Sweden^Atrium Ljungberg            
Sweden^Study association Vuksenskolan Halland            
Sweden^Pilotage            
Sweden^Holy Cross            
Sweden^Smiling Faces             
Sweden^Ensolution            
Sweden^Wikström AB            
Sweden^Lemontree Enterprise Solutions AB            
Sweden^Sundbom &amp; Partners            
Sweden^Cadence Design Systems AB            
Sweden^Curitiba AB            
Sweden^SDS Life Science &amp; SDS MedteQ            
Sweden^SmartaVal AB            
Sweden^HELP Insurance            
Sweden^Net gain            
Sweden^Citedo AB            
Sweden^Atrium Ljungberg
Sweden^Tre
Sweden^AbbVie
Sweden^Tyréns
Sweden^AB Stångåstaden
Sweden^Multisoft AB
Sweden^Synoptik Sweden AB
Sweden^Studieförbundet Vuxenskolan Halland
Sweden^Wihlborgs Fastigheter AB
Sweden^Transcendent Group
Sweden^Sundbom &amp; Partners
Sweden^Tenant &amp; Partner
Sweden^Centiro
Sweden^Hilti
Europe^Europe
Europe^DHL Express
Europe^AbbVie
Europe^Cisco
Europe^Salesforce
Europe^Hilton
Europe^Hilti
Europe^Amgen
Europe^SAS Institute
Europe^The Adecco Group
Europe^Sopra Steria
Europe^Specsavers
Europe^Grohe
Europe^Roche
Europe^SC Johnson
Europe^Stryker
Europe^Cadence
Europe^Admiral Group
Europe^Novo Nordisk
Europe^Adobe
Europe^Volkswagen Financial Services
Europe^Bristol-Myers Squibb
Europe^Accuracy
Europe^LGT Group
Europe^Homeserve
Europe^Teleperformance
Europe^Chiesi Group
Europe^Fronius
Europe^Deloitte
Europe^Admiral Group plc
Europe^Groupe SEB
Europe^Atos
Europe^Insight
Europe^Ipsen
Europe^Liberty Mutual
Europe^Biogen
Ireland^Intact
Ireland^Agilent Technologies
Ireland^Serosep Limited
Ireland^Ballinlough
Ireland^Block, Inc
Ireland^WP Engine Ireland Ltd
Ireland^Crewit Resourcing Group
Ireland^Amryt Pharma
Ireland^CORA Systems
Ireland^Marymount
Ireland^Nathan Trust 
Ireland^Riot Games
Ireland^Legato Health Technologies Ireland Ltd.
Ireland^Broadridge Financial Solutions
Ireland^Decathlon Ireland
Ireland^ETU
Ireland^Grenke Limited
Ireland^Loxam Access
Ireland^Walls to Workstations
Ireland^capSpire
Ireland^Gather &amp; Gather
Ireland^Keane's CarePlus Pharmacy Group
Ireland^Alcon
Ireland^B. Braun Medical Ltd. (Naas Road)
Ireland^CACI Non-Life
Ireland^Clio
Ireland^Core
Ireland^Datalex
Ireland^Dental Tech
Ireland^Equinix
Ireland^Global
Ireland^Guidewire
Ireland^Loxam Rental
Ireland^Mainstream Renewable Power
Ireland^Midlands Park Hotel
Ireland^ORS
Ireland^Regeneron Ireland
Ireland^Taoglas
Ireland^The Doyle Collection
Ireland^Unum
Ireland^Volkswagen Group Ireland
Ireland^AbbVie Ireland
Ireland^3Dental
Ireland^Asana
Ireland^Bewley's
Ireland^Capital Switchgear
Ireland^Cairn Homes 
Ireland^Certification Europe
Ireland^Citco Ireland
Ireland^CluneTech
Ireland^Cpl Ireland
Ireland^Crown Roofing and Cladding Ltd
Ireland^Distilled.
Ireland^Dornan Engineering Limited
Ireland^Edwards Lifesciences
Ireland^Esri Ireland
Ireland^Expleo
Ireland^Glenveagh Properties PLC
Ireland^H&amp;R Block Global Technology Center Ireland
Ireland^Hilton
Ireland^Informatica
Ireland^Irish Rugby Football Union
Ireland^JTI Ireland Ltd
Ireland^Kuehne + Nagel
Ireland^Laya Healthcare
Ireland^Ogier Leman
Ireland^Lennox
Ireland^Liferay
Ireland^LotusWorks
Ireland^Lundbeck Ireland Ltd
Ireland^Meaghers Pharmacy
Ireland^Morgan McKinley
Ireland^Office of Government Procurement
Ireland^PEI
Ireland^Paycheck Plus
Ireland^Portwest Head Office
Ireland^Prepay Power
Ireland^Scurri
Ireland^Squarespace
Ireland^Towercom
Ireland^Verus Metrology Partners
Ireland^Advanz Pharma
Ireland^ACB Group
Ireland^Avant Money
Ireland^ATA Tools Limited
Ireland^Cisco Ireland
Ireland^Codex
Ireland^Consilient Health
Ireland^DHL Express (Ireland) Ltd
Ireland^ESW
Ireland^Fiserv Nenagh
Ireland^Fáilte Ireland
Ireland^Global Shares Ireland Ltd
Ireland^Horizon Therapeutics
Ireland^IPB Insurance
Ireland^Liberty IT
Ireland^MSD Dunboyne 
Ireland^Net Affinity 
Ireland^Office of the Comptroller and Auditor General
Ireland^Osborne
Ireland^Plan International Ireland
Ireland^ServiceNow Ireland
Ireland^Promed
Ireland^Tesco Ireland
Ireland^Toast 
Ireland^WaterWipes
Ireland^Woodie's
Ireland^Workhuman
Ireland^Adobe Ireland
Ireland^Cadence
Ireland^Charles River Ireland
Ireland^Childhood Development Initiative
Ireland^Fisher Investments Ireland
Ireland^Genesys
Ireland^Mitchell McDermott
Ireland^Northside Home Care Services
Ireland^Seetec Ireland
Ireland^Statkraft Ireland
Ireland^Udemy Ireland Ltd.
Ireland^BMS Cruiserath Biologics
Ireland^Propylon
Ireland^Avvio
Ireland^Cloudera
Ireland^Salesforce
Ireland^BlackBerry
Ireland^Coupa Software
Ireland^DHL Global Forwarding
Ireland^DHL Supply Chain
Ireland^Eurofins Scientific (Ireland) Limited
Ireland^Experian
Ireland^Liberty Insurance
Ireland^Next Generation
Ireland^Tayto Snacks
Ireland^Version 1
Ireland^Citrix Ireland
Ireland^Granite Digital
Ireland^H&R Block Global Technology Center Ireland
Ireland^Poppulo
Global Culture^Google
Global Culture^Adobe
Global Culture^Samsung
Global Culture^Microsoft
Global Culture^HubSpot
Global Culture^Chegg
Global Culture^Meta
Global Culture^Elsevier
Global Culture^Boston Consulting Group
Global Culture^Concentrix
Global Culture^Sage
Global Culture^Zoom Video Communications
Global Culture^Amazon
Global Culture^Apple
Global Culture^Trimble
Global Culture^TaskUs
Global Culture^IBM
Global Culture^Medallia
Global Culture^LexisNexis Legal Professional
Global Culture^Dynatrace
Global Culture^RingCentral
Global Culture^Meltwater
Global Culture^DXC Technology
Global Culture^adidas
Global Culture^PepsiCo
Global Culture^SentinelOne
Global Culture^GE Power
Global Culture^Guidewire Software
Global Culture^Conduent
Global Culture^Gympass
Global Culture^SAP
Global Culture^Dell Technologies
Global Culture^Everbridge
Global Culture^Cornerstone OnDemand
Global Culture^Siemens
Global Culture^Nu Skin Enterprises
Global Culture^Vista
Global Culture^ADP
Global Culture^Thomson Reuters
Global Culture^Uber
Global Culture^Sitecore
Global Culture^Fanatics Commerce
Global Culture^T-Mobile
Global Culture^Calix
Global Culture^HP Inc.
Global Culture^IPC Systems
Global Culture^Philips
Global Culture^Pipedrive
Global Culture^Phenom
Global Culture^Cisco


'''
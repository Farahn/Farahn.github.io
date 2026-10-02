#!/usr/bin/env python3
"""Build script for Dr Farah Nadeem's website.

All content lives in the lists below. To add a publication, talk or project,
edit the matching list and run:

    python3 build.py

This regenerates index.html, llms.txt, robots.txt and sitemap.xml in the
folder above this one. Keep editing here rather than in index.html, so the
page, the structured data and the AI-readable summary stay in sync.
"""
import base64
import html
import json
import os

SITE_URL = "https://farahn.github.io/"   # change if you use a custom domain
UPDATED = "2026-10-02"
UPDATED_LABEL = "October 2026"
EMAIL = "farah_nadeem@lums.edu.pk"
ORCID_ID = "0000-0001-9241-1592"

TITLE = "Dr Farah Nadeem | AI, education data and equity | LUMS"
DESCRIPTION = ("Dr Farah Nadeem, Assistant Professor at the LUMS School of Education, Pakistan, "
               "researches AI, education data systems, assessment and fair access to school.")

PROFILES = [
    ("Google Scholar", "https://scholar.google.com/citations?user=j5Pahl4AAAAJ&hl=en"),
    ("LinkedIn", "https://www.linkedin.com/in/farah-nadeem/"),
    ("GitHub", "https://github.com/Farahn"),
    ("LUMS profile", "https://lums.edu.pk/lums_employee/9543"),
    ("dblp", "https://dblp.org/pid/145/3081.html"),
    ("ORCID", "https://orcid.org/0000-0001-9241-1592"),
]

BIO_SHORT = ("Dr Farah Nadeem is an Assistant Professor at the LUMS School of Education in Lahore, Pakistan. "
             "Her research uses machine learning and large-scale education data to study assessment, teacher "
             "development and fair access to school. She holds a PhD in Electrical and Computer Engineering "
             "from the University of Washington, where she was a Fulbright Fellow.")

BIO_LONG = [
    "Dr Farah Nadeem is an Assistant Professor at the Syed Ahsan Ali and Syed Maratib Ali School of Education "
    "at the Lahore University of Management Sciences (LUMS). Her research brings machine learning and education "
    "data to questions of assessment, teaching quality and fair access to school.",
    "She leads studies funded by the UK Foreign, Commonwealth and Development Office on the political economy of "
    "assessment data, responsible AI in education and the simulation of school enrolment, and is co-principal "
    "investigator on a Google Society-Centered AI Research Award. Earlier, she led monitoring and evaluation for "
    "Punjab's school education reform programme, where her team ran data collection for 52,000 schools, and she "
    "has worked with UNICEF Pakistan and the World Bank's Education Global Practice. From 2023 to 2025 she "
    "directed the LUMS Office of Accessibility and Inclusion.",
    "She holds a PhD in Electrical and Computer Engineering from the University of Washington, where she was a "
    "Fulbright Fellow.",
]

# ---------------------------------------------------------------- areas
AREAS = {
    "a": {"name": "AI and data science"},
    "b": {"name": "Education systems and policy"},
    "c": {"name": "Equity and inclusion"},
}

REGIONS = {
    "a": {"label": "AI and data science",
          "text": "Projects here use machine learning, language technology, simulation and large-scale data."},
    "b": {"label": "Education systems and policy",
          "text": "Projects here study assessment, teacher development, data use and governance in school systems."},
    "c": {"label": "Equity and inclusion",
          "text": "Projects here ask who gets to learn, across gender, disability, location and income."},
    "ab": {"label": "Assessment and data systems",
           "text": "Projects here measure learning and teaching more accurately and make system data useful to the people who run schools."},
    "ac": {"label": "Responsible and fair AI",
           "text": "Projects here test whether AI works fairly for communities and languages it was not designed around."},
    "bc": {"label": "Access and inclusion",
           "text": "Projects here examine how institutions and policies widen access and participation."},
    "abc": {"label": "All three areas",
            "text": "Projects here combine modelling, system data and an equity lens to inform policy."},
}
CHIP_ORDER = ["", "a", "b", "c", "ab", "ac", "bc", "abc"]

# ---------------------------------------------------------------- projects
DARE = "UK FCDO, through DARE-RC"
SOE_NOV = "https://soe.lums.edu.pk/news/data-inclusion-and-resilience-advancing-equity-pakistans-education-systems-through-evidence"
SOE_SEP = "https://soe.lums.edu.pk/news/policy-dialogue-school-education-explores-teacher-effectiveness-and-workforce-management"
DOORWAY = "https://darerc.org/the-digital-doorway-bridging-the-gap-between-observation-and-support/"

PROJECTS = [
    {
        "id": "equity-equation", "short": "Equity Equation Project", "areas": "abc", "when": "Ongoing", "kind": "Research",
        "title": "The Equity Equation Project",
        "meta": [("Role", "Principal investigator"), ("Funding", DARE), ("Partner", "CITY@LUMS")],
        "desc": ["This project brings existing data sources together in a GIS framework and uses agent-based "
                 "simulation to test how policy choices could change school enrolment for different groups of "
                 "children in Lahore. The aim is to show planners which barriers keep children out of school and "
                 "which interventions would reach them. Results presented in 2025 point to economic barriers as a "
                 "major constraint on access."],
        "outputs": [("Talk", "Predictive modelling of policy impact on school enrolment, 2025", SOE_NOV),
                    ("Video", "Using simulation and data to shape education policy, 2025", "https://darerc.org/videos/"),
                    ("Code", "Model repository on GitHub", "https://github.com/Farahn/EEP")],
    },
    {
        "id": "responsible-ai", "short": "Responsible AI scoping study", "areas": "abc", "when": "Ongoing", "kind": "Research",
        "title": "Responsible AI Integration in Education in Pakistan: A Scoping Study",
        "meta": [("Role", "Principal investigator"), ("Funding", DARE), ("Team", "Dr Maryam Mustafa and Annum Sadiq")],
        "desc": ["The study maps current and emerging uses of AI in Pakistani education across Punjab, Sindh and "
                 "the Islamabad Capital Territory. It benchmarks national policy against international frameworks "
                 "and gathers evidence from teachers, EdTech firms and civil society on equity, governance and safe "
                 "implementation. The study held a National Convening on Responsible AI in Education at the Pakistan "
                 "Institute of Education, Islamabad, in August 2026."],
        "outputs": [],
    },
    {
        "id": "beyond-western-defaults", "short": "Beyond Western Defaults", "areas": "ac", "when": "Awarded 2026", "kind": "Research",
        "title": "Beyond Western Defaults: A Socio-Technical Infrastructure for Community-Governed AI Alignment in Low-Resource Contexts",
        "meta": [("Role", "Co-principal investigator"), ("Principal investigator", "Dr Maryam Mustafa"),
                 ("Funding", "Google Society-Centered AI Research Award")],
        "desc": ["Large language models already give health, education and legal guidance in Pakistan, yet the "
                 "benchmarks that decide whether they work reflect Western linguistic and cultural defaults. This "
                 "project builds infrastructure through which communities in low-resource settings can govern how AI "
                 "systems are aligned and evaluated. It is grounded in two deployments: Awaaz-e-Sehat, a voice-enabled "
                 "maternal health platform, and a speech-first literacy and numeracy app for out-of-school adolescent "
                 "girls in Punjab and Khyber Pakhtunkhwa."],
        "outputs": [],
    },
    {
        "id": "assessment-data", "short": "Assessment data use study", "areas": "ab", "when": "Ongoing", "kind": "Research",
        "title": "Political Economy Analysis of Assessment Data Use in Pakistan",
        "meta": [("Role", "Principal investigator"), ("Funding", DARE)],
        "desc": ["This study examines how political and institutional incentives shape the production, "
                 "interpretation and use of assessment data across federal, provincial and district levels of "
                 "Pakistan's education system. It combines predictive modelling with a multi-tier political economy "
                 "analysis to identify where assessment data informs decisions and where it does not."],
        "outputs": [("Paper", "Navigating the landscape of multiple data sources, IAEA 2026", "#pub-iaea-2026")],
    },
    {
        "id": "teacher-development", "short": "Punjab CPD study", "areas": "ab", "when": "2025 to 2026", "kind": "Research",
        "title": "Digital Evolution in Teacher Development: Punjab's Continuous Professional Development System",
        "meta": [("Role", "Researcher, classroom observation strand"), ("Lead researcher", "Nighat Lone, DARE-RC"),
                 ("Funding", DARE)],
        "desc": ["This mixed-methods study traces how Punjab's digitised professional development system moves "
                 "information between classrooms, mentors and the provincial secretariat. It combines classroom "
                 "observation data from 2021 onwards in four districts with fieldwork in 24 schools. Data travels "
                 "upward quickly, but support and feedback rarely travel back to teachers, and training content often "
                 "misses the realities of multigrade and multilingual classrooms."],
        "outputs": [("Blog", "The digital doorway, 2026", DOORWAY),
                    ("Policy brief", "Digital evolution in teacher development, 2026", "#pub-cpd-brief"),
                    ("Paper", "From data to decisions, AERA 2025", "#pub-aera-cot"),
                    ("Talk", "Policy dialogue on teacher effectiveness, 2025", SOE_SEP)],
    },
    {
        "id": "urdu-reading", "short": "Urdu reading assessment pilot", "areas": "ab", "when": "Pilot, 2026", "kind": "Research",
        "title": "Automated Assessment of Urdu Oral Reading Fluency",
        "meta": [("Focus", "Children aged 7 to 10 reading Urdu"),
                 ("Method", "Speech recognition benchmarked against expert scoring")],
        "desc": ["This pilot benchmarks multilingual speech recognition models on recordings of children reading "
                 "Urdu passages, comparing automated words-correct-per-minute scores with expert human scoring. "
                 "Errors are analysed by age, gender, school location and passage difficulty. The results will "
                 "inform a costed plan for an offline, teacher-facing tool for formative reading assessment."],
        "outputs": [],
    },
    {
        "id": "gender-equity", "short": "Gender equity mapping", "areas": "bc", "when": "Institutional review", "kind": "Research",
        "title": "Gender Equity Mapping Survey at LUMS",
        "meta": [("Role", "Principal investigator"), ("Funding", "LUMS")],
        "desc": ["This university-wide review assesses the state of gender equality in LUMS policies, culture and "
                 "practice, drawing on primary and secondary research."],
        "outputs": [("Related paper", "Breaking barriers and biases, AERA 2025", "#pub-aera-gender")],
    },
    {
        "id": "doctoral-research", "short": "Doctoral research", "areas": "abc", "when": "2016 to 2020", "kind": "Research",
        "title": "Language Use in K-16 STEM Education (Doctoral Research)",
        "meta": [("Institution", "University of Washington"), ("Advisor", "Professor Mari Ostendorf"),
                 ("Funding", "US$500K NSF grant that I helped write")],
        "desc": ["My dissertation developed natural language processing tools to analyse language in K-16 STEM "
                 "materials and validated them against student performance. It estimated the linguistic complexity "
                 "of science texts and assessment items, measured the representation and agency of feminine and "
                 "masculine characters in K-12 texts, and showed that item features such as linguistic complexity "
                 "have non-linear effects on item difficulty. The work rested on a formal partnership between "
                 "Electrical and Computer Engineering and the College of Education."],
        "outputs": [("Thesis", "Automatic analysis of language use in K-16 STEM education, 2020", "#pub-thesis"),
                    ("Paper", "Estimating linguistic complexity for science texts, BEA 2018", "#pub-bea-2018"),
                    ("Paper", "Language based mapping of science assessment items to skills, BEA 2017", "#pub-bea-2017"),
                    ("Code", "Linguistic complexity models", "https://github.com/Farahn/Liguistic-Complexity"),
                    ("Code", "BCA text classifier", "https://github.com/Farahn/BCA")],
    },
    {
        "id": "essay-scoring", "short": "Automated essay scoring", "areas": "ab", "when": "2018 to 2019", "kind": "Research",
        "title": "Automated Essay Scoring with Discourse-Aware Models",
        "meta": [("Setting", "Research internship, Liulishuo, San Mateo, California")],
        "desc": ["This work built neural essay scoring models for English language learners that account for text "
                 "coherence, reducing the need for hand-crafted features and human scoring. The goal was writing "
                 "feedback that resource-constrained classrooms could use at scale."],
        "outputs": [("Paper", "Automated essay scoring with discourse-aware neural models, BEA 2019", "#pub-bea-2019"),
                    ("Code", "Essay scoring repository", "https://github.com/Farahn/AES")],
    },
    {
        "id": "accessibility-office", "short": "Office of Accessibility and Inclusion", "areas": "bc", "when": "2023 to 2025", "kind": "Practice",
        "title": "Office of Accessibility and Inclusion, LUMS",
        "meta": [("Role", "Director")],
        "desc": ["I directed the campus-wide office responsible for academic accommodations, accessibility and "
                 "inclusion for students, faculty and staff, serving a community of more than 6,000 people. The "
                 "office developed institutional policy on accessibility and accommodations and supported student "
                 "resilience through the Be REAL programme."],
        "outputs": [("Programme", "Be REAL, developed at the University of Washington", "https://ccfwb.uw.edu/bereal/")],
    },
    {
        "id": "punjab-data", "short": "Punjab school data systems", "areas": "ab", "when": "2020 to 2021", "kind": "Practice",
        "title": "School Data Systems for Punjab",
        "meta": [("Role", "Monitoring and Evaluation Specialist"),
                 ("Organisation", "Programme Monitoring and Implementation Unit, Punjab Education Sector Reforms Programme")],
        "desc": ["I led the monitoring and evaluation team that ran end-to-end data collection for 52,000 public "
                 "schools across Punjab. We introduced unique identifiers for 11 million students so that records "
                 "could be tracked over time and linked across data systems for planning and research."],
        "outputs": [("Report", "Annual School Census Report 2020-21", "#pub-census")],
    },
]

# ---------------------------------------------------------------- publications
PUB_TYPES = [("", "All"), ("paper", "Peer-reviewed papers"), ("presentation", "Conference presentations"),
             ("report", "Reports and briefs"), ("thesis", "Thesis")]

PUBS = [
    {"id": "pub-iaea-2026", "year": 2026, "type": "presentation",
     "title": "Navigating the Landscape of Multiple Data Sources for Educational Reporting in LMICs: The Case of Pakistan",
     "authors": "S. Maheen, I. Muzaffar, and F. Nadeem",
     "venue": "51st Annual Conference of the International Association for Educational Assessment (IAEA), Toronto, 2026",
     "href": None, "links": [("Conference", "https://www.eqao.com/iaea-annual-conference/")],
     "project": "assessment-data",
     "cite": "Maheen, S., Muzaffar, I., & Nadeem, F. (2026). Navigating the landscape of multiple data sources for "
             "educational reporting in LMICs: The case of Pakistan [Paper presentation]. 51st Annual Conference of "
             "the International Association for Educational Assessment, Toronto, Canada."},
    {"id": "pub-cpd-brief", "year": 2026, "type": "report",
     "title": "Digital Evolution in Teacher Development: Analysis of Punjab's Continuous Professional Development (CPD) System",
     "authors": "N. Lone, F. Nadeem, J. Albrent, and N. Tariq",
     "venue": "Policy brief, Data and Research in Education Research Consortium (DARE-RC), 2026",
     "href": None, "links": [("Study page", "https://darerc.org/research-at-glance/")],
     "project": "teacher-development",
     "cite": "Lone, N., Nadeem, F., Albrent, J., & Tariq, N. (2026). Digital evolution in teacher development: Analysis "
             "of Punjab's continuous professional development (CPD) system [Policy brief]. Data and Research in "
             "Education Research Consortium."},
    {"id": "pub-aera-cot", "year": 2025, "type": "presentation",
     "title": "From Data to Decisions: Rethinking Classroom Observation Metrics for Effective Education Reform in Punjab, Pakistan",
     "authors": "F. Nadeem, J. C. Albrent, M. Fatima, Y. Arif, S. E. Zahra, and A. Mahmood",
     "venue": "Annual Meeting of the American Educational Research Association (AERA), 2025",
     "href": None, "links": [], "project": "teacher-development",
     "cite": "Nadeem, F., Albrent, J. C., Fatima, M., Arif, Y., Zahra, S. E., & Mahmood, A. (2025). From data to "
             "decisions: Rethinking classroom observation metrics for effective education reform in Punjab, Pakistan "
             "[Paper presentation]. Annual Meeting of the American Educational Research Association."},
    {"id": "pub-aera-gender", "year": 2025, "type": "presentation",
     "title": "Breaking Barriers and Biases: Understanding Female Student Experiences in University Extracurricular Activities and Student Leadership Roles",
     "authors": "A. Rehman, A. Hussain, and F. Nadeem",
     "venue": "Annual Meeting of the American Educational Research Association (AERA), 2025",
     "href": None, "links": [], "project": "gender-equity",
     "cite": "Rehman, A., Hussain, A., & Nadeem, F. (2025). Breaking barriers and biases: Understanding female student "
             "experiences in university extracurricular activities and student leadership roles [Paper presentation]. "
             "Annual Meeting of the American Educational Research Association."},
    {"id": "pub-census", "year": 2021, "type": "report",
     "title": "Annual School Census Report 2020-21",
     "authors": "F. Nadeem",
     "venue": "School Education Department, Government of the Punjab, April 2021",
     "href": "https://www.pesrp.edu.pk/downloads/school_census/2020_21/School_Census_Report_2020_21.pdf",
     "links": [("PDF", "https://www.pesrp.edu.pk/downloads/school_census/2020_21/School_Census_Report_2020_21.pdf")],
     "project": "punjab-data",
     "cite": "Nadeem, F. (2021). Annual school census report 2020-21. School Education Department, Government of the Punjab."},
    {"id": "pub-thesis", "year": 2020, "type": "thesis",
     "title": "Automatic Analysis of Language Use in K-16 STEM Education and Impact on Student Performance",
     "authors": "F. Nadeem",
     "venue": "PhD dissertation, University of Washington, 2020",
     "href": "https://digital.lib.washington.edu/researchworks/items/492a6dda-c1fa-4289-9991-b4ee25b8072f",
     "links": [("ResearchWorks", "https://digital.lib.washington.edu/researchworks/items/492a6dda-c1fa-4289-9991-b4ee25b8072f")],
     "project": "doctoral-research",
     "cite": "Nadeem, F. (2020). Automatic analysis of language use in K-16 STEM education and impact on student "
             "performance [Doctoral dissertation, University of Washington]. ResearchWorks Archive."},
    {"id": "pub-bea-2019", "year": 2019, "type": "paper",
     "title": "Automated Essay Scoring with Discourse-Aware Neural Models",
     "authors": "F. Nadeem, H. Nguyen, Y. Liu, and M. Ostendorf",
     "venue": "Proceedings of the Fourteenth Workshop on Innovative Use of NLP for Building Educational Applications (BEA), Florence, 2019, pages 484-493",
     "href": "https://aclanthology.org/W19-4450/", "doi": "10.18653/v1/W19-4450",
     "links": [("PDF", "https://aclanthology.org/W19-4450.pdf"), ("DOI", "https://doi.org/10.18653/v1/W19-4450"),
               ("Code", "https://github.com/Farahn/AES")],
     "project": "essay-scoring",
     "cite": "Nadeem, F., Nguyen, H., Liu, Y., & Ostendorf, M. (2019). Automated essay scoring with discourse-aware "
             "neural models. In Proceedings of the Fourteenth Workshop on Innovative Use of NLP for Building "
             "Educational Applications (pp. 484-493). Association for Computational Linguistics. "
             "https://doi.org/10.18653/v1/W19-4450"},
    {"id": "pub-bea-2018", "year": 2018, "type": "paper",
     "title": "Estimating Linguistic Complexity for Science Texts",
     "authors": "F. Nadeem and M. Ostendorf",
     "venue": "Proceedings of the Thirteenth Workshop on Innovative Use of NLP for Building Educational Applications (BEA), New Orleans, 2018, pages 45-55",
     "href": "https://aclanthology.org/W18-0505/", "doi": "10.18653/v1/W18-0505",
     "links": [("PDF", "https://aclanthology.org/W18-0505.pdf"), ("DOI", "https://doi.org/10.18653/v1/W18-0505"),
               ("Code", "https://github.com/Farahn/Liguistic-Complexity")],
     "project": "doctoral-research",
     "cite": "Nadeem, F., & Ostendorf, M. (2018). Estimating linguistic complexity for science texts. In Proceedings "
             "of the Thirteenth Workshop on Innovative Use of NLP for Building Educational Applications (pp. 45-55). "
             "Association for Computational Linguistics. https://doi.org/10.18653/v1/W18-0505"},
    {"id": "pub-bea-2017", "year": 2017, "type": "paper",
     "title": "Language Based Mapping of Science Assessment Items to Skills",
     "authors": "F. Nadeem and M. Ostendorf",
     "venue": "Proceedings of the 12th Workshop on Innovative Use of NLP for Building Educational Applications (BEA), Copenhagen, 2017, pages 319-326",
     "href": "https://aclanthology.org/W17-5036/", "doi": "10.18653/v1/W17-5036",
     "links": [("PDF", "https://aclanthology.org/W17-5036.pdf"), ("DOI", "https://doi.org/10.18653/v1/W17-5036")],
     "project": "doctoral-research",
     "cite": "Nadeem, F., & Ostendorf, M. (2017). Language based mapping of science assessment items to skills. In "
             "Proceedings of the 12th Workshop on Innovative Use of NLP for Building Educational Applications "
             "(pp. 319-326). Association for Computational Linguistics. https://doi.org/10.18653/v1/W17-5036"},
    # earlier engineering work, shown in a collapsible group
    {"id": "pub-wns3-2016", "year": 2016, "type": "paper", "earlier": True,
     "title": "Investigation and Improvements to the OFDM Wi-Fi Physical Layer Abstraction in ns-3",
     "authors": "H. Safavi-Naeini, F. Nadeem, and S. Roy",
     "venue": "Proceedings of the Workshop on ns-3 (WNS3), 2016, pages 65-70",
     "href": None, "links": [],
     "cite": "Safavi-Naeini, H., Nadeem, F., & Roy, S. (2016). Investigation and improvements to the OFDM Wi-Fi "
             "physical layer abstraction in ns-3. In Proceedings of the Workshop on ns-3 (pp. 65-70)."},
    {"id": "pub-ntms-2014", "year": 2014, "type": "paper", "earlier": True,
     "title": "Measurement Based Call Admission Control (CAC) to Improve QoS for IEEE 802.11e WLAN",
     "authors": "A. Hussain, N. ul Hassan, and F. Nadeem",
     "venue": "6th International Conference on New Technologies, Mobility and Security (NTMS), 2014",
     "href": None, "links": [],
     "cite": "Hussain, A., ul Hassan, N., & Nadeem, F. (2014). Measurement based call admission control (CAC) to "
             "improve QoS for IEEE 802.11e WLAN. In 6th International Conference on New Technologies, Mobility and "
             "Security (NTMS)."},
    {"id": "pub-ijwin-2014", "year": 2014, "type": "paper", "earlier": True,
     "title": "Saturation Throughput Analysis of IEEE 802.11e EDCA through Analytical Model",
     "authors": "M. F. Usman, A. Hussain, and F. Nadeem",
     "venue": "International Journal of Wireless Information Networks, 21(2), pages 101-113, 2014",
     "href": None, "links": [],
     "cite": "Usman, M. F., Hussain, A., & Nadeem, F. (2014). Saturation throughput analysis of IEEE 802.11e EDCA "
             "through analytical model. International Journal of Wireless Information Networks, 21(2), 101-113."},
]

# ---------------------------------------------------------------- writing and talks
TALKS = [
    {"id": "talk-summit-2026", "date": "2026-10-31", "label": "31 Oct 2026", "type": "Talk",
     "title": "Data, AI and Evidence for Better Decision-Making",
     "detail": "Thematic briefing, DARE-RC International Education Summit 2026, LUMS, Lahore",
     "href": "https://darerc.org/education-summit-2026/", "linktext": "Summit programme"},
    {"id": "talk-language-2026", "date": "2026-09-29", "label": "29 Sep 2026", "type": "Moderator",
     "title": "AI and Language Learning: Possibilities, Limitations and Risks",
     "detail": "Plenary session, Policy Dialogue on Language, Literacy and Learning, GRADES-STP and TALEEM Programme, Lahore"},
    {"id": "blog-digital-doorway", "date": "2026-03-30", "label": "30 Mar 2026", "type": "Blog",
     "title": "The Digital Doorway: Bridging the Gap Between Observation and Support",
     "detail": "DARE-RC blog, with Areej Mahmood and Nighat Lone",
     "href": DOORWAY, "linktext": "Read the post"},
    {"id": "talk-enrolment-2025", "date": "2025-11-28", "label": "28 Nov 2025", "type": "Talk",
     "title": "Predictive Modelling of Policy Impact on School Enrolment",
     "detail": "Policy dialogue on data, inclusion and resilience, LUMS School of Education with DARE-RC, Lahore",
     "href": SOE_NOV, "linktext": "Event report"},
    {"id": "talk-cpd-2025", "date": "2025-09-24", "label": "24 Sep 2025", "type": "Talk",
     "title": "The Digital Evolution in Teacher Development: Analysis of Punjab's CPD System",
     "detail": "Policy dialogue on teacher effectiveness and workforce management, LUMS School of Education with DARE-RC, Lahore",
     "href": SOE_SEP, "linktext": "Event report"},
    {"id": "talk-symposium-2025", "date": "2025-02-19", "label": "19 Feb 2025", "type": "Talk",
     "title": "Using Simulation and Data to Shape Education Policy",
     "detail": "DARE-RC Research Symposium, Islamabad",
     "href": "https://darerc.org/videos/", "linktext": "Watch on DARE-RC"},
    {"id": "video-data-governance", "date": None, "label": "Video", "type": "Talk",
     "title": "Academia, Public and Private Collaboration for Ethical Data Governance",
     "detail": "DARE-RC video series",
     "href": "https://darerc.org/videos/", "linktext": "Watch on DARE-RC"},
    {"id": "talk-podcast-2021", "date": "2021-09", "label": "Sep 2021", "type": "Podcast",
     "title": "As a Woman of Color in STEM",
     "detail": "Fulbright Women Podcast",
     "href": "https://www.youtube.com/watch?v=NhYpHp4jVrY", "linktext": "Listen on YouTube"},
    {"id": "talk-fulbright-2019", "date": "2019-10", "label": "Oct 2019", "type": "Talk",
     "title": "Machine Learning Tools for K-12 STEM Assessments",
     "detail": "Annual Fulbright Conference, Arlington, Virginia"},
    {"id": "talk-thrive-2018", "date": "2018-03", "label": "Mar 2018", "type": "Talk",
     "title": "Earning the Privilege to Thrive",
     "detail": "Western Washington Fulbright Talks, Seattle"},
    {"id": "talk-equity-2017", "date": "2017-03", "label": "Mar 2017", "type": "Talk",
     "title": "Empowerment and Equity: Starting with Perceptions",
     "detail": "Western Washington Fulbright Talks, Seattle"},
]

# ---------------------------------------------------------------- teaching, leadership, about
COURSES = [
    ("Impact Evaluation Methods for Education", "Graduate course"),
    ("Applied Data Analysis", "Graduate course"),
    ("Practicum Proseminar", "Graduate course"),
    ("Results-Based Management", "Professional workshop"),
    ("Monitoring, Evaluation and Learning for Leadership", "Professional workshop"),
]
TEACHING_NOTE = ("I also run workshops for government and practitioner audiences, most recently on AI literacy for "
                 "researchers in the DARE-RC study circle and on competency-based assessment for senior officials at "
                 "the Punjab Education Curriculum, Training and Assessment Authority.")

LEADERSHIP = [
    ("2023 to 2025", "Director, Office of Accessibility and Inclusion, LUMS", None),
    ("2026", "Co-led the launch of the Assessment, Insight and Measurement Collective (AIMC) at the School of Education", None),
    ("Current", "Co-facilitator, Be REAL student resilience programme", None),
    ("2018 to 2020", "Chair (2019 to 2020) and member, Provost Advisory Committee for Students, University of Washington, "
                     "including task forces on student mental health and on data science for non-STEM majors", None),
    ("2019 to 2020", "Co-creator, Electrical and Computer Engineering Student Advisory Committee, University of Washington",
     "https://www.ece.uw.edu/ecesac/"),
    ("2018 to 2019", "Co-chair, Student Research Workshop, North American Chapter of the Association for Computational Linguistics", None),
    ("2017 to 2020", "Advocate for student parents and caregivers, University of Washington", None),
    ("2019", "Selection panel member, Western Washington Fulbright Talks", None),
]
REVIEWING = ("Peer reviewer since 2018 for the AERA Annual Meeting, Language Resources and Evaluation (Springer), "
             "IEEE Transactions on Systems, Man, and Cybernetics: Systems, the BEA workshop, AACL-IJCNLP 2020 and EMNLP.")

EXPERIENCE = [
    ("2023 to present", "Assistant Professor", "Syed Ahsan Ali and Syed Maratib Ali School of Education, LUMS", None),
    ("2023 to 2025", "Director, Office of Accessibility and Inclusion", "LUMS", None),
    ("2023 to 2025", "Education Consultant", "World Bank, Education Global Practice",
     "Supported a global analytical report on tertiary education that builds on STEERing Tertiary Education."),
    ("2021 to 2023", "Education Technology and MIS Expert", "UNICEF Pakistan, Islamabad",
     "Supported education data systems and foundational literacy and numeracy programmes, and learning frameworks for Punjab and Khyber Pakhtunkhwa."),
    ("2020 to 2021", "Monitoring and Evaluation Specialist", "PMIU, Punjab Education Sector Reforms Programme, Lahore", None),
    ("2018", "Research Intern", "Liulishuo, San Mateo, California", None),
    ("2016 to 2019", "Engineering Fellow and STEM Career Mentor", "School districts in Western Washington and the Yakima Valley", None),
    ("2008 to 2009", "Research Assistant", "Canada Pakistan Basic Education Project, CIDA, Lahore", None),
]

EDUCATION = [
    ("2020", "PhD, Electrical and Computer Engineering", "University of Washington, Seattle. Fulbright Fellow. Dissertation committee chair: Professor Mari Ostendorf."),
    ("2014", "MS, Electrical Engineering", "National University of Computer and Emerging Sciences (FAST-NUCES), Lahore"),
    ("2008", "BS, Electrical Engineering", "National University of Sciences and Technology (NUST), Islamabad"),
]

AWARDS = [
    ("2026", "Google Society-Centered AI Research Award, as co-principal investigator", None),
    ("2015 to 2020", "Fulbright Fellowship for doctoral study", None),
    ("2019", "Husky 100, University of Washington", "https://www.ece.uw.edu/spotlight/two-ece-students-selected-for-the-husky-100/"),
    ("2019", "Homecoming Scholar, University of Washington", None),
    ("2019 and 2020", "Celebrate: UW Women", None),
    ("2016 to 2017", "Engineering Fellow, Washington STEM with Washington MESA", None),
]

METHODS = ("Machine learning and natural language processing in Python (TensorFlow, scikit-learn, pandas), "
           "predictive and agent-based modelling, impact evaluation and mixed-methods research, with analysis in R and Stata.")

KNOWS_ABOUT = ["Machine learning in education", "Natural language processing", "Educational assessment",
               "Education data systems", "Education policy in Pakistan", "Responsible AI in education",
               "Agent-based modelling", "Teacher professional development", "Equity and inclusion in education",
               "Impact evaluation", "Accessibility in higher education"]

# ================================================================ helpers
def e(s):
    return html.escape(str(s), quote=True)


GLYPH_POS = {"a": (9.75, 8.4), "b": (16.25, 8.4), "c": (13.0, 14.03)}


def glyph(areas, cls="glyph", labelled=True):
    circles = []
    for k in "abc":
        x, y = GLYPH_POS[k]
        klass = f"g-on g-{k}" if k in areas else "g-off"
        circles.append(f'<circle class="{klass}" cx="{x}" cy="{y}" r="6.5"/>')
    if labelled:
        names = ", ".join(AREAS[k]["name"] for k in "abc" if k in areas)
        return (f'<svg class="{cls}" viewBox="0 0 26 22" role="img" aria-label="Areas: {e(names)}">'
                f'<title>Areas: {e(names)}</title>{"".join(circles)}</svg>')
    return f'<svg class="{cls}" viewBox="0 0 26 22" aria-hidden="true" focusable="false">{"".join(circles)}</svg>'


def project_html(p):
    meta = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in p["meta"])
    desc = "".join(f"<p>{e(x)}</p>" for x in p["desc"])
    outs = ""
    if p["outputs"]:
        items = "".join(f'<li><span class="o-type">{e(t)}</span> <a href="{e(h)}">{e(txt)}</a></li>'
                        for t, txt, h in p["outputs"])
        outs = f'<ul class="outputs" aria-label="Outputs and links for this project">{items}</ul>'
    kind = f'<p class="p-kind">{e(p["kind"])}</p>' if p["kind"] != "Research" else ""
    return (f'<article class="project" id="{p["id"]}" data-areas="{p["areas"]}">'
            f'<div class="p-rail">{glyph(p["areas"])}<p class="p-when">{e(p["when"])}</p>{kind}</div>'
            f'<div class="p-body"><h3>{e(p["title"])}</h3><dl class="p-meta">{meta}</dl>{desc}{outs}</div>'
            f'</article>')


PROJECT_SHORT = {p["id"]: p["short"] for p in PROJECTS}


def pub_html(p):
    authors = e(p["authors"]).replace("F. Nadeem", "<strong>F. Nadeem</strong>")
    title = f'<a href="{e(p["href"])}">{e(p["title"])}</a>' if p.get("href") else e(p["title"])
    links = "".join(f'<a href="{e(h)}">{e(t)}</a>' for t, h in p.get("links", []))
    proj = ""
    if p.get("project"):
        proj = f'<a href="#{p["project"]}">Project: {e(PROJECT_SHORT[p["project"]])}</a>'
    cid = "cite-" + p["id"]
    cite_btn = (f'<button type="button" class="link-btn js-only" aria-expanded="false" '
                f'aria-controls="{cid}" data-cite-toggle>Cite</button>')
    cite_box = (f'<div class="cite-box" id="{cid}" hidden><p class="cite-text">{e(p["cite"])}</p>'
                f'<button type="button" class="small-btn" data-copy="{e(p["cite"])}" data-done="Citation copied">'
                f'Copy citation</button></div>')
    search = " ".join([p["title"], p["authors"], p["venue"], str(p["year"])]).lower()
    return (f'<li class="pub" id="{p["id"]}" data-type="{p["type"]}" data-search="{e(search)}">'
            f'<p class="pub-title">{title}</p><p class="pub-authors">{authors}</p>'
            f'<p class="pub-venue">{e(p["venue"])}</p>'
            f'<p class="pub-actions">{links}{proj}{cite_btn}</p>{cite_box}</li>')


def pub_groups(items):
    years = sorted({p["year"] for p in items}, reverse=True)
    out = []
    for y in years:
        lis = "".join(pub_html(p) for p in items if p["year"] == y)
        out.append(f'<div class="pub-year"><h3 class="year">{y}</h3><ol class="pub-list">{lis}</ol></div>')
    return "".join(out)


def talk_html(t):
    date_attr = f' data-date="{t["date"]}"' if t.get("date") else ""
    link = f' <a href="{e(t["href"])}">{e(t["linktext"])}</a>' if t.get("href") else ""
    return (f'<li class="talk" id="{t["id"]}"{date_attr} data-title="{e(t["title"])}" data-detail="{e(t["detail"])}">'
            f'<p class="t-date">{e(t["label"])}</p>'
            f'<div class="t-body"><p class="t-type">{e(t["type"])}</p><p class="t-title">{e(t["title"])}</p>'
            f'<p class="t-detail">{e(t["detail"])}.{link}</p></div></li>')


def chip_html(key, group="area"):
    if group == "area":
        label = "All areas" if key == "" else REGIONS[key]["label"]
        g = glyph(key, cls="glyph chip-glyph", labelled=False) if key else ""
        pressed = "true" if key == "" else "false"
        return f'<button type="button" class="chip" data-set="{key}" aria-pressed="{pressed}">{g}<span>{e(label)}</span></button>'
    raise ValueError(group)


def region_counts():
    counts = {}
    for k in REGIONS:
        counts[k] = sum(1 for p in PROJECTS if all(ch in p["areas"] for ch in k))
    return counts


# ================================================================ venn svg
VENN = """
<svg class="venn" id="venn" viewBox="78 0 484 560" role="img" aria-labelledby="venn-t venn-d">
  <title id="venn-t">Map of research areas</title>
  <desc id="venn-d">Three overlapping circles labelled AI and data science, Education systems and policy, and Equity and inclusion. Their overlaps are assessment and data systems, responsible and fair AI, and access and inclusion. The centre holds work that draws on all three.</desc>
  <defs>
    <clipPath id="clip-a"><circle cx="245" cy="230" r="150"/></clipPath>
    <clipPath id="clip-b"><circle cx="395" cy="230" r="150"/></clipPath>
    <clipPath id="clip-c"><circle cx="320" cy="360" r="150"/></clipPath>
    <mask id="venn-mask" maskUnits="userSpaceOnUse" x="0" y="0" width="640" height="560"></mask>
  </defs>
  <g class="v-fill">
    <circle class="f-a" cx="245" cy="230" r="150"/>
    <circle class="f-b" cx="395" cy="230" r="150"/>
    <circle class="f-c" cx="320" cy="360" r="150"/>
    <g clip-path="url(#clip-b)"><circle class="f-ab" cx="245" cy="230" r="150"/></g>
    <g clip-path="url(#clip-c)"><circle class="f-ac" cx="245" cy="230" r="150"/></g>
    <g clip-path="url(#clip-c)"><circle class="f-bc" cx="395" cy="230" r="150"/></g>
    <g clip-path="url(#clip-b)"><g clip-path="url(#clip-c)"><circle class="f-abc" cx="245" cy="230" r="150"/></g></g>
  </g>
  <g class="v-stroke">
    <circle class="s-a" cx="245" cy="230" r="150"/>
    <circle class="s-b" cx="395" cy="230" r="150"/>
    <circle class="s-c" cx="320" cy="360" r="150"/>
  </g>
  <rect class="v-veil" x="0" y="0" width="640" height="560" mask="url(#venn-mask)"/>
  <g class="v-hl"></g>
  <g class="v-labels" aria-hidden="true">
    <text class="l-dom l-a" x="96" y="36"><tspan x="96">AI and</tspan><tspan x="96" dy="25">data science</tspan></text>
    <text class="l-dom l-b" x="544" y="36" text-anchor="end"><tspan x="544">Education systems</tspan><tspan x="544" dy="25">and policy</tspan></text>
    <text class="l-dom l-c" x="320" y="542" text-anchor="middle">Equity and inclusion</text>
    <text class="l-in" x="320" y="174" text-anchor="middle"><tspan x="320">Assessment and</tspan><tspan x="320" dy="17">data systems</tspan></text>
    <text class="l-in" x="227" y="336" text-anchor="middle"><tspan x="227">Responsible</tspan><tspan x="227" dy="17">and fair AI</tspan></text>
    <text class="l-in" x="413" y="336" text-anchor="middle"><tspan x="413">Access and</tspan><tspan x="413" dy="17">inclusion</tspan></text>
    <text class="l-in l-core" x="320" y="286" text-anchor="middle">All three</text>
  </g>
</svg>
"""

THEME_ICON = ('<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" focusable="false">'
              '<circle cx="12" cy="12" r="8.25" fill="none" stroke="currentColor" stroke-width="1.8"/>'
              '<path d="M12 3.75a8.25 8.25 0 0 1 0 16.5z" fill="currentColor"/></svg>')

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
           "%3Ccircle cx='24' cy='25' r='17' fill='%232F55D4' fill-opacity='.85'/%3E"
           "%3Ccircle cx='40' cy='25' r='17' fill='%230C7068' fill-opacity='.85'/%3E"
           "%3Ccircle cx='32' cy='39' r='17' fill='%23E0A52E' fill-opacity='.85'/%3E%3C/svg%3E")

# ================================================================ css
CSS = r"""
*,*::before,*::after{box-sizing:border-box}
[hidden]{display:none!important}
.nw{white-space:nowrap}
:root{
  color-scheme:light;
  --font:"Public Sans","Atkinson Hyperlegible Next","Atkinson Hyperlegible",ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;
  --ground:#F7F8F6; --ground-2:#EDF0EC; --ink:#18233F; --ink-2:#46516B; --line:#D3D9D4; --line-strong:#9AA4B5;
  --a:#2F55D4; --b:#0C7068; --c:#946000; --link:#2F55D4; --focus:#C2185B;
  --r-a:#DCE4FB; --r-b:#D2EEE8; --r-c:#FBE6C1; --r-ab:#B9D3EE; --r-ac:#D9CBEE; --r-bc:#D5E8B4; --r-abc:#2B44A8; --r-abc-ink:#FFFFFF;
  --g-blend:multiply; --badge:#FBE6C1;
  --rail:11rem; --gap:2.25rem;
  box-sizing:border-box;
  padding-top:env(safe-area-inset-top,0px);
  padding-bottom:env(safe-area-inset-bottom,0px);
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    color-scheme:dark;
    --ground:#0F1626; --ground-2:#151E31; --ink:#E8ECF4; --ink-2:#A8B2C6; --line:#27324A; --line-strong:#56627C;
    --a:#8FA8FF; --b:#5ED0C2; --c:#F0BE55; --link:#9DB4FF; --focus:#FF7AB8;
    --r-a:#1B2856; --r-b:#0E3833; --r-c:#3A2D0D; --r-ab:#1D4A6B; --r-ac:#392C62; --r-bc:#34461A; --r-abc:#A9BCFF; --r-abc-ink:#0F1626;
    --g-blend:screen; --badge:#4A3A12;
  }
}
:root[data-theme="dark"]{
  color-scheme:dark;
  --ground:#0F1626; --ground-2:#151E31; --ink:#E8ECF4; --ink-2:#A8B2C6; --line:#27324A; --line-strong:#56627C;
  --a:#8FA8FF; --b:#5ED0C2; --c:#F0BE55; --link:#9DB4FF; --focus:#FF7AB8;
  --r-a:#1B2856; --r-b:#0E3833; --r-c:#3A2D0D; --r-ab:#1D4A6B; --r-ac:#392C62; --r-bc:#34461A; --r-abc:#A9BCFF; --r-abc-ink:#0F1626;
  --g-blend:screen; --badge:#4A3A12;
}
html{scroll-padding-top:calc(env(safe-area-inset-top,0px) + 5.5rem);-webkit-text-size-adjust:100%;text-size-adjust:100%}
@media (max-width:900px){html{scroll-padding-top:calc(env(safe-area-inset-top,0px) + 7.5rem)}}
@media (prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--font);font-size:1.0625rem;line-height:1.6;
  font-weight:400;font-optical-sizing:auto;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
img,svg{max-width:100%}
a{color:var(--link);text-decoration-thickness:1px;text-underline-offset:.2em}
a:hover{text-decoration-thickness:2px}
:focus-visible{outline:3px solid var(--focus);outline-offset:3px;border-radius:4px}
p{margin:0}
h1,h2,h3{margin:0;font-weight:800;line-height:1.15}
abbr[title]{text-decoration:none}
.wrap{max-width:76rem;margin-inline:auto;padding-inline:clamp(1.25rem,4vw,2.75rem)}
.visually-hidden{position:absolute!important;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}
.no-js .js-only{display:none!important}

/* skip link */
.skip{position:absolute;left:1rem;top:-5rem;z-index:50;background:var(--ink);color:var(--ground);padding:.75rem 1rem;border-radius:8px;font-weight:700;text-decoration:none}
.skip:focus{top:calc(env(safe-area-inset-top,0px) + .75rem)}

/* header */
.site-header{position:sticky;top:env(safe-area-inset-top,0px);z-index:30;background:var(--ground);border-bottom:1px solid transparent;transition:border-color .2s}
.site-header.is-scrolled{border-bottom-color:var(--line)}
.header-inner{display:flex;align-items:center;gap:1.25rem;min-height:4.25rem}
.brand{display:inline-flex;align-items:center;gap:.6rem;color:var(--ink);text-decoration:none;font-weight:800;font-size:1.0625rem;letter-spacing:-.01em;white-space:nowrap;padding:.4rem 0}
.brand .glyph{width:2rem;height:auto}
.site-nav{margin-left:auto;min-width:0}
.site-nav ul{display:flex;gap:.15rem;list-style:none;margin:0;padding:0}
.site-nav a{display:block;padding:.6rem .7rem;color:var(--ink-2);text-decoration:none;font-weight:700;font-size:.9375rem;border-radius:8px;white-space:nowrap}
.site-nav a:hover{color:var(--ink);background:var(--ground-2)}
.site-nav a[aria-current="true"]{color:var(--ink);box-shadow:inset 0 -3px 0 var(--ink);border-radius:8px 8px 2px 2px}
.theme-toggle{flex:none;width:2.75rem;height:2.75rem;display:grid;place-items:center;border:1.5px solid var(--line-strong);border-radius:50%;background:transparent;color:var(--ink);cursor:pointer;padding:0}
.theme-toggle:hover{border-color:var(--ink)}
@media (max-width:900px){
  .header-inner{flex-wrap:wrap;gap:0 1rem;padding-top:.35rem}
  .theme-toggle{margin-left:auto}
  .site-nav{order:3;width:100%;margin-left:0;overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch;
    margin-inline:calc(-1 * clamp(1.25rem,4vw,2.75rem));padding-inline:clamp(.6rem,3vw,2rem);width:calc(100% + 2 * clamp(1.25rem,4vw,2.75rem))}
  .site-nav::-webkit-scrollbar{display:none}
  .site-nav ul{padding-bottom:.35rem}
}

/* hero */
.hero{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.08fr);gap:clamp(2rem,5vw,4.5rem);align-items:center;
  padding-block:clamp(1.5rem,4vw,3rem) clamp(2.5rem,6vw,4.5rem)}
.hero h1{font-size:clamp(3.1rem,8.2vw,6.25rem);line-height:.92;letter-spacing:-.04em;margin:0 0 1.25rem}
.hero h1 span{display:block}
.portrait{display:block;width:clamp(5rem,9vw,7.5rem);height:auto;aspect-ratio:1/1;border-radius:50%;object-fit:cover;margin:0 0 1.6rem;box-shadow:0 0 0 1px var(--line)}
.hero-role{font-size:clamp(1.05rem,1.6vw,1.2rem);font-weight:700;color:var(--ink-2);margin:0 0 1.6rem}
.hero-statement{font-size:clamp(1.45rem,2.7vw,2.05rem);line-height:1.3;font-weight:350;letter-spacing:-.012em;max-width:27ch;margin:0 0 1.4rem}
.hero-note{color:var(--ink-2);max-width:44ch;margin:0 0 1.75rem}
.hero-links{display:flex;flex-wrap:wrap;gap:.6rem;list-style:none;margin:0;padding:0}
.hero-links a{display:inline-flex;align-items:center;min-height:2.85rem;padding:0 1.1rem;border:1.5px solid var(--ink);border-radius:10px;color:var(--ink);font-weight:700;text-decoration:none}
.hero-links a:hover{background:var(--ground-2)}
.hero-links li:first-child a{background:var(--ink);color:var(--ground)}
.hero-links li:first-child a:hover{background:var(--ink-2);border-color:var(--ink-2)}
.hero-next{margin-top:1.6rem;font-size:.9375rem;color:var(--ink-2);max-width:48ch}
.hero-next strong{color:var(--ink)}
@media (max-width:880px){.hero{grid-template-columns:1fr}.hero-statement{max-width:32ch}}

/* venn */
.venn-figure{margin:0;width:100%;max-width:33rem;justify-self:center}
.venn{display:block;width:100%;height:auto;overflow:visible;touch-action:manipulation;-webkit-tap-highlight-color:transparent}
.venn.is-over{cursor:pointer}
.f-a{fill:var(--r-a)}.f-b{fill:var(--r-b)}.f-c{fill:var(--r-c)}
.f-ab{fill:var(--r-ab)}.f-ac{fill:var(--r-ac)}.f-bc{fill:var(--r-bc)}.f-abc{fill:var(--r-abc)}
.v-stroke circle{fill:none;stroke-width:2.5}
.s-a{stroke:var(--a)}.s-b{stroke:var(--b)}.s-c{stroke:var(--c)}
.v-veil{fill:var(--ground);opacity:0;transition:opacity .25s ease;pointer-events:none}
.venn.has-sel .v-veil{opacity:.68}
.v-hl,.v-labels{pointer-events:none}
.o-sel circle{fill:none;stroke:var(--ink);stroke-width:4.5}
.o-hover circle{fill:none;stroke:var(--ink);stroke-width:2.5;stroke-dasharray:7 6}
.v-labels text{font-family:var(--font)}
.l-dom{font-size:22px;font-weight:800;letter-spacing:-.01em}
.l-a{fill:var(--a)}.l-b{fill:var(--b)}.l-c{fill:var(--c)}
.l-in{font-size:14px;font-weight:700;fill:var(--ink)}
.l-core{font-size:17px;font-weight:800;fill:var(--r-abc-ink)}
@media (max-width:560px){.l-in{display:none}.l-dom{font-size:25px}}
.venn-caption{margin:.9rem 0 0;min-height:5.2em;font-size:.9688rem;color:var(--ink-2)}
.venn-caption strong{color:var(--ink)}
.venn-caption a{font-weight:700;white-space:nowrap}
@media (prefers-reduced-motion:no-preference){
  .js .v-stroke circle{stroke-dasharray:943;stroke-dashoffset:943;animation:draw 1s cubic-bezier(.3,.7,.2,1) forwards}
  .js .v-stroke .s-b{animation-delay:.15s}
  .js .v-stroke .s-c{animation-delay:.3s}
  .js .v-fill,.js .v-labels{opacity:0;animation:fadein .7s ease .75s forwards}
  @keyframes draw{to{stroke-dashoffset:0}}
  @keyframes fadein{to{opacity:1}}
}

/* glyphs */
.glyph .g-on{fill-opacity:.9;mix-blend-mode:var(--g-blend)}
.glyph .g-a{fill:var(--a)}.glyph .g-b{fill:var(--b)}.glyph .g-c{fill:var(--c)}
.glyph .g-off{fill:none;stroke:var(--ink-2);stroke-width:1.1;stroke-opacity:.75}

/* sections */
.section{padding-block:clamp(3.5rem,8vw,6.5rem)}
.band{background:var(--ground-2)}
.section-head{display:grid;grid-template-columns:var(--rail) minmax(0,1fr);gap:1rem var(--gap);margin-bottom:2.25rem}
.section-head > *{grid-column:2}
.section-head > h2{grid-column:1 / -1;font-size:clamp(2rem,4vw,2.75rem);letter-spacing:-.03em}
.section-intro{max-width:62ch;color:var(--ink-2)}
.indent{padding-left:calc(var(--rail) + var(--gap))}
@media (max-width:820px){
  .section-head{grid-template-columns:1fr;gap:.75rem}
  .section-head > *{grid-column:1}
  .indent{padding-left:0}
}

/* chips and controls */
.control-label{font-weight:700;font-size:.9375rem;margin:0 0 .6rem;display:block}
.chips{display:flex;flex-wrap:wrap;gap:.5rem}
.chip{display:inline-flex;align-items:center;gap:.5rem;min-height:2.75rem;padding:.35rem .9rem .35rem .65rem;border:1.5px solid var(--line-strong);
  border-radius:10px;background:var(--ground);color:var(--ink);font:inherit;font-size:.9375rem;font-weight:700;line-height:1.2;cursor:pointer;text-align:left}
.chip[data-set=""],.chip[data-type]{padding-left:.9rem}
.chip:hover{border-color:var(--ink)}
.chip[aria-pressed="true"]{background:var(--ink);border-color:var(--ink);color:var(--ground)}
.chip-glyph{width:1.6rem;height:auto;flex:none}
.chip[aria-pressed="true"] .g-off{stroke:var(--ground);stroke-opacity:.9}
.chip[aria-pressed="true"] .g-on{mix-blend-mode:normal;stroke:var(--ground);stroke-width:.8}
.count{margin-top:1rem;font-size:.9375rem;color:var(--ink-2);font-weight:700}

/* projects */
.projects{display:grid;gap:3.25rem;margin-top:2.75rem}
.project{display:grid;grid-template-columns:var(--rail) minmax(0,1fr);gap:var(--gap)}
.p-rail{display:flex;flex-direction:column;align-items:flex-start;gap:.55rem;padding-top:.15rem}
.p-rail .glyph{width:3.4rem;height:auto}
.p-when{font-size:.9375rem;font-weight:700;color:var(--ink-2)}
.p-kind{font-size:.875rem;font-weight:700;color:var(--ink);background:var(--badge);padding:.1rem .5rem;border-radius:6px}
.project h3{font-size:clamp(1.2rem,2.1vw,1.45rem);letter-spacing:-.015em;line-height:1.25;max-width:44ch;margin-bottom:.7rem}
.p-meta{display:flex;flex-wrap:wrap;gap:.2rem 1.4rem;margin:0 0 .9rem;font-size:.9375rem}
.p-meta div{display:flex;gap:.35rem}
.p-meta dt{color:var(--ink-2)}
.p-meta dt::after{content:":"}
.p-meta dd{margin:0;font-weight:700}
.p-body > p{max-width:68ch;margin-bottom:1rem}
.outputs{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:.45rem 1.4rem;font-size:.9375rem}
.o-type{color:var(--ink-2);font-weight:700;margin-right:.2rem}
.project:target .p-body,.pub:target,.talk:target .t-body{animation:flash 2.2s ease}
@keyframes flash{0%,35%{background:var(--badge);box-shadow:0 0 0 .6rem var(--badge)}100%{background:transparent;box-shadow:0 0 0 .6rem transparent}}
@media (max-width:820px){
  .project{grid-template-columns:1fr;gap:.75rem}
  .p-rail{flex-direction:row;align-items:center;gap:.8rem}
  .p-rail .glyph{width:2.6rem}
}

/* publications */
.pub-tools{display:grid;gap:1.1rem;margin-bottom:2.25rem}
.search-field input{width:min(100%,28rem);min-height:2.85rem;padding:.5rem .9rem;border:1.5px solid var(--line-strong);border-radius:10px;
  background:var(--ground);color:var(--ink);font:inherit}
.search-field input:hover{border-color:var(--ink)}
.band .chip,.band .search-field input{background:var(--ground-2)}
.band .chip[aria-pressed="true"]{background:var(--ink)}
.pub-year{display:grid;grid-template-columns:var(--rail) minmax(0,1fr);gap:var(--gap);padding-block:1.1rem}
.year{font-size:1.75rem;font-weight:300;color:var(--ink-2);letter-spacing:-.02em;line-height:1.1}
.pub-list{list-style:none;margin:0;padding:0;display:grid;gap:1.75rem}
.pub{border-radius:4px}
.pub-title{font-weight:700;font-size:1.0625rem;line-height:1.4;margin-bottom:.3rem;max-width:68ch}
.pub-title a{color:var(--ink);text-decoration-color:var(--line-strong)}
.pub-title a:hover{color:var(--link);text-decoration-color:currentColor}
.pub-authors,.pub-venue{font-size:.9375rem;color:var(--ink-2);max-width:72ch}
.pub-authors strong{color:var(--ink)}
.pub-actions{display:flex;flex-wrap:wrap;align-items:center;gap:.35rem 1.1rem;margin-top:.5rem;font-size:.9375rem}
.link-btn{font:inherit;font-weight:700;color:var(--link);background:none;border:0;padding:.2rem 0;cursor:pointer;
  text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:.2em;min-height:1.75rem}
.link-btn:hover{text-decoration-thickness:2px}
.cite-box{margin-top:.75rem;padding:1rem 1.1rem;border:1.5px solid var(--line-strong);border-radius:10px;max-width:72ch;display:grid;gap:.75rem;justify-items:start}
.cite-text{font-size:.9375rem;user-select:all;-webkit-user-select:all}
.small-btn{font:inherit;font-size:.9375rem;font-weight:700;min-height:2.5rem;padding:.3rem .9rem;border:1.5px solid var(--ink);border-radius:8px;background:transparent;color:var(--ink);cursor:pointer}
.small-btn:hover{background:var(--ink);color:var(--ground)}
.empty{font-weight:700;margin:1rem 0}
.earlier{margin-top:1.5rem}
.earlier summary{cursor:pointer;font-weight:700;min-height:2.75rem;display:flex;align-items:center;gap:.6rem;width:fit-content}
.earlier summary::marker{content:""}
.earlier summary::-webkit-details-marker{display:none}
.earlier summary::before{content:"+";display:inline-grid;place-items:center;width:1.6rem;height:1.6rem;border:1.5px solid currentColor;border-radius:50%;font-weight:800;line-height:1}
.earlier[open] summary::before{content:"\2212"}
@media (max-width:820px){.pub-year{grid-template-columns:1fr;gap:.6rem}}

/* talks */
.talks{list-style:none;margin:0;padding:0;display:grid;gap:1.6rem}
.talk{display:grid;grid-template-columns:var(--rail) minmax(0,1fr);gap:var(--gap)}
.t-date{font-weight:700;color:var(--ink-2);font-size:.9375rem;font-variant-numeric:tabular-nums;padding-top:.1rem}
.t-type{font-size:.875rem;font-weight:700;color:var(--ink-2);display:flex;gap:.5rem;align-items:center;flex-wrap:wrap}
.badge{display:inline-block;background:var(--badge);color:var(--ink);border-radius:6px;padding:0 .45rem;font-size:.8125rem;font-weight:800}
.t-title{font-weight:700;font-size:1.0625rem;line-height:1.4;margin:.1rem 0 .2rem;max-width:62ch}
.t-detail{font-size:.9375rem;color:var(--ink-2);max-width:72ch}
.t-detail a{font-weight:700;white-space:nowrap}
@media (max-width:820px){.talk{grid-template-columns:1fr;gap:.2rem}}

/* teaching and leadership, about */
.cols{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:2.75rem 3.5rem}
.cols h3,.about-facts h3{font-size:1.2rem;letter-spacing:-.01em;margin-bottom:1rem}
.plain{list-style:none;margin:0;padding:0;display:grid;gap:.95rem}
.plain .what{font-weight:700;display:block;line-height:1.4}
.plain .meta{display:block;font-size:.9375rem;color:var(--ink-2)}
.note{margin-top:1.25rem;color:var(--ink-2);max-width:62ch;font-size:.9688rem}
.dated{list-style:none;margin:0;padding:0;display:grid;gap:1rem}
.dated li{display:grid;grid-template-columns:8.75rem minmax(0,1fr);gap:1rem}
.dated .when{font-size:.9375rem;font-weight:700;color:var(--ink-2);font-variant-numeric:tabular-nums;padding-top:.05rem}
.dated .what{font-weight:700;display:block;line-height:1.4}
.dated .meta{display:block;font-size:.9375rem;color:var(--ink-2)}
@media (max-width:820px){.cols{grid-template-columns:1fr}}
@media (max-width:520px){.dated li{grid-template-columns:1fr;gap:.1rem}}
.bio p{max-width:66ch;margin-bottom:1rem;font-size:1.125rem;line-height:1.65}
.bio p:first-child{font-size:clamp(1.2rem,2vw,1.35rem);line-height:1.5}
.copy-row{display:flex;flex-wrap:wrap;gap:.6rem;margin:1.5rem 0 3.25rem}
.about-facts{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:2.75rem 3.5rem}
.about-facts .stack{display:grid;gap:2.5rem;align-content:start}
@media (max-width:900px){.about-facts{grid-template-columns:1fr}}

/* contact */
.contact{background:var(--ink);color:var(--ground)}
.contact a{color:var(--ground)}
.contact :focus-visible{outline-color:var(--ground)}
.contact .section-intro{color:var(--ground);opacity:.85}
.email-big{display:inline-block;font-size:clamp(1.45rem,4.6vw,3.1rem);font-weight:800;letter-spacing:-.03em;line-height:1.15;overflow-wrap:anywhere;margin:.25rem 0 2rem}
.profiles{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:.6rem 1.6rem;font-weight:700}
.profiles a{display:inline-block;padding:.35rem 0}
.site-footer{margin-top:clamp(3rem,7vw,5rem);padding-top:1.5rem;border-top:1px solid color-mix(in srgb,var(--ground) 25%,transparent);
  display:flex;flex-wrap:wrap;gap:.6rem 2.5rem;font-size:.9375rem;opacity:.9}
.site-footer p{max-width:60ch}

/* toast */
.toast{position:fixed;left:50%;bottom:calc(env(safe-area-inset-bottom,0px) + 1.25rem);transform:translate(-50%,1rem);z-index:60;
  background:var(--ink);color:var(--ground);padding:.75rem 1.1rem;border-radius:10px;font-weight:700;font-size:.9375rem;
  opacity:0;pointer-events:none;transition:opacity .2s,transform .2s;max-width:calc(100vw - 2rem)}
.toast.is-on{opacity:1;transform:translate(-50%,0)}

@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{animation-duration:.001ms!important;animation-iteration-count:1!important;transition-duration:.001ms!important}
}
@media print{
  .site-header,.filters,.pub-tools,.theme-toggle,.venn-figure,.toast,.copy-row,.skip,.hero-note,[data-cite-toggle]{display:none!important}
  body{background:#fff;color:#000;font-size:11pt}
  .band,.contact{background:#fff;color:#000}
  .contact a,a{color:#000}
  .project[hidden],.pub[hidden],.pub-year[hidden]{display:grid!important}
  .section{padding-block:1.5rem}
  .hero{display:block;padding-block:1rem}
}
"""

# ================================================================ js
JS = r"""
(function () {
  'use strict';
  var root = document.documentElement;
  var REGIONS = /*REGIONS*/;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  /* theme */
  var themeBtn = document.getElementById('theme-toggle');
  var darkQuery = window.matchMedia('(prefers-color-scheme: dark)');
  function isDark() { var t = root.getAttribute('data-theme'); return t ? t === 'dark' : darkQuery.matches; }
  function syncTheme() { if (themeBtn) themeBtn.setAttribute('aria-pressed', isDark() ? 'true' : 'false'); }
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var next = isDark() ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (err) {}
      syncTheme();
    });
  }
  if (darkQuery.addEventListener) darkQuery.addEventListener('change', syncTheme);
  syncTheme();

  /* toast and copy */
  var toastEl = document.getElementById('toast');
  var toastTimer;
  function toast(msg) {
    if (!toastEl) return;
    toastEl.textContent = msg;
    toastEl.classList.add('is-on');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.classList.remove('is-on'); }, 2600);
  }
  function legacyCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text; ta.setAttribute('readonly', '');
    ta.style.position = 'fixed'; ta.style.top = '0'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.select();
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (err) {}
    document.body.removeChild(ta);
    return ok;
  }
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text).then(function () { return true; }, function () { return legacyCopy(text); });
    }
    return Promise.resolve(legacyCopy(text));
  }
  document.addEventListener('click', function (ev) {
    var btn = ev.target.closest('[data-copy]');
    if (btn) {
      copyText(btn.getAttribute('data-copy')).then(function (ok) {
        toast(ok ? (btn.getAttribute('data-done') || 'Copied') : 'Copying is blocked in this browser. Select the text and copy it.');
      });
      return;
    }
    var cite = ev.target.closest('[data-cite-toggle]');
    if (cite) {
      var box = document.getElementById(cite.getAttribute('aria-controls'));
      var open = cite.getAttribute('aria-expanded') === 'true';
      cite.setAttribute('aria-expanded', open ? 'false' : 'true');
      if (box) box.hidden = open;
    }
  });

  /* venn map and project filter */
  var svg = document.getElementById('venn');
  var NS = 'http://www.w3.org/2000/svg';
  var CENTRES = { a: [245, 230], b: [395, 230], c: [320, 360] };
  var R = 150;
  var projects = Array.prototype.slice.call(document.querySelectorAll('.project'));
  var chips = Array.prototype.slice.call(document.querySelectorAll('#research .chip'));
  var countEl = document.getElementById('project-count');
  var caption = document.getElementById('venn-caption');
  var selected = '';
  var hover = '';

  function matches(p, key) {
    var areas = p.getAttribute('data-areas');
    for (var i = 0; i < key.length; i++) { if (areas.indexOf(key[i]) === -1) return false; }
    return true;
  }
  function countFor(key) { return projects.filter(function (p) { return matches(p, key); }).length; }
  function plural(n) { return n === 1 ? '1 project' : n + ' projects'; }

  function el(tag, attrs) {
    var node = document.createElementNS(NS, tag);
    for (var k in attrs) node.setAttribute(k, attrs[k]);
    return node;
  }
  function circleFor(k, attrs) {
    var a = { cx: CENTRES[k][0], cy: CENTRES[k][1], r: R };
    for (var x in attrs) a[x] = attrs[x];
    return el('circle', a);
  }
  function clipWrap(node, others) {
    others.forEach(function (o) { var g = el('g', { 'clip-path': 'url(#clip-' + o + ')' }); g.appendChild(node); node = g; });
    return node;
  }
  function intersection(key, attrs) {
    var ks = key.split('');
    return clipWrap(circleFor(ks[0], attrs), ks.slice(1));
  }
  function outline(key, cls) {
    var g = el('g', { 'class': cls });
    key.split('').forEach(function (k) {
      g.appendChild(clipWrap(circleFor(k, {}), key.split('').filter(function (o) { return o !== k; })));
    });
    return g;
  }
  function drawVenn() {
    if (!svg) return;
    var hl = svg.querySelector('.v-hl');
    var mask = svg.querySelector('#venn-mask');
    while (hl.firstChild) hl.removeChild(hl.firstChild);
    while (mask.firstChild) mask.removeChild(mask.firstChild);
    if (selected) {
      mask.appendChild(el('rect', { x: 0, y: 0, width: 640, height: 560, fill: 'white' }));
      mask.appendChild(intersection(selected, { fill: 'black' }));
      hl.appendChild(outline(selected, 'o-sel'));
      svg.classList.add('has-sel');
    } else {
      svg.classList.remove('has-sel');
    }
    if (hover && hover !== selected) hl.appendChild(outline(hover, 'o-hover'));
  }
  function setCaption() {
    if (!caption) return;
    var key = hover || selected;
    caption.textContent = '';
    if (!key) {
      caption.textContent = 'Select an area or an overlap to filter the projects below.';
      return;
    }
    var r = REGIONS[key];
    var strong = document.createElement('strong');
    strong.textContent = r.label + '. ';
    caption.appendChild(strong);
    caption.appendChild(document.createTextNode(r.text + ' '));
    var n = countFor(key);
    if (key === selected) {
      var a = document.createElement('a');
      a.href = '#research';
      a.textContent = 'See the ' + plural(n);
      caption.appendChild(a);
    } else {
      var s = document.createElement('span');
      s.textContent = plural(n) + '.';
      caption.appendChild(s);
    }
  }
  function applyFilter(key) {
    selected = key;
    var n = 0;
    projects.forEach(function (p) { var ok = !key || matches(p, key); p.hidden = !ok; if (ok) n++; });
    chips.forEach(function (c) { c.setAttribute('aria-pressed', c.getAttribute('data-set') === key ? 'true' : 'false'); });
    if (countEl) {
      countEl.textContent = key
        ? 'Showing ' + n + ' of ' + projects.length + ' projects in ' + REGIONS[key].label + '.'
        : 'Showing all ' + projects.length + ' projects.';
    }
    drawVenn();
    setCaption();
  }
  function regionAt(ev) {
    var m = svg.getScreenCTM();
    if (!m) return '';
    var pt = svg.createSVGPoint();
    pt.x = ev.clientX; pt.y = ev.clientY;
    var p = pt.matrixTransform(m.inverse());
    var key = '';
    'abc'.split('').forEach(function (k) {
      var dx = p.x - CENTRES[k][0], dy = p.y - CENTRES[k][1];
      if (dx * dx + dy * dy <= R * R) key += k;
    });
    return key;
  }
  if (svg) {
    svg.addEventListener('pointermove', function (ev) {
      if (ev.pointerType === 'touch') return;
      var k = regionAt(ev);
      if (k !== hover) { hover = k; svg.classList.toggle('is-over', !!k); drawVenn(); setCaption(); }
    });
    svg.addEventListener('pointerleave', function () { hover = ''; svg.classList.remove('is-over'); drawVenn(); setCaption(); });
    svg.addEventListener('click', function (ev) {
      var k = regionAt(ev);
      if (!k) return;
      hover = '';
      applyFilter(k === selected ? '' : k);
    });
  }
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      var k = c.getAttribute('data-set');
      applyFilter(k === selected && k !== '' ? '' : k);
    });
    function enter() { var k = c.getAttribute('data-set'); if (k) { hover = k; drawVenn(); setCaption(); } }
    function leave() { hover = ''; drawVenn(); setCaption(); }
    c.addEventListener('mouseenter', enter);
    c.addEventListener('mouseleave', leave);
    c.addEventListener('focus', enter);
    c.addEventListener('blur', leave);
  });
  if (countEl) countEl.textContent = 'Showing all ' + projects.length + ' projects.';
  setCaption();

  /* publications */
  var pubSearch = document.getElementById('pub-search');
  var pubChips = Array.prototype.slice.call(document.querySelectorAll('#publications .chip'));
  var pubs = Array.prototype.slice.call(document.querySelectorAll('.pub'));
  var pubCount = document.getElementById('pub-count');
  var pubEmpty = document.getElementById('pub-empty');
  var earlier = document.getElementById('earlier-work');
  var pubType = '';
  function filterPubs() {
    var q = pubSearch ? pubSearch.value.trim().toLowerCase() : '';
    var n = 0;
    pubs.forEach(function (p) {
      var ok = (!pubType || p.getAttribute('data-type') === pubType) && (!q || p.getAttribute('data-search').indexOf(q) !== -1);
      p.hidden = !ok;
      if (ok) n++;
    });
    Array.prototype.forEach.call(document.querySelectorAll('.pub-year'), function (g) {
      g.hidden = !g.querySelector('.pub:not([hidden])');
    });
    if (earlier) {
      var any = !!earlier.querySelector('.pub:not([hidden])');
      earlier.hidden = !any;
      if (q && any) earlier.open = true;
    }
    if (pubEmpty) pubEmpty.hidden = n !== 0;
    if (pubCount) {
      pubCount.textContent = (q || pubType)
        ? 'Showing ' + n + ' of ' + pubs.length + ' publications.'
        : 'Showing all ' + pubs.length + ' publications.';
    }
  }
  if (pubSearch) pubSearch.addEventListener('input', filterPubs);
  pubChips.forEach(function (c) {
    c.addEventListener('click', function () {
      pubType = c.getAttribute('data-type');
      pubChips.forEach(function (o) { o.setAttribute('aria-pressed', o === c ? 'true' : 'false'); });
      filterPubs();
    });
  });
  filterPubs();

  /* reveal a linked item that a filter has hidden */
  function revealTarget(id) {
    var t = document.getElementById(id);
    if (!t) return;
    if (t.classList.contains('project') && t.hidden) applyFilter('');
    if (t.classList.contains('pub') && t.hidden) {
      if (pubSearch) pubSearch.value = '';
      pubType = '';
      pubChips.forEach(function (o) { o.setAttribute('aria-pressed', o.getAttribute('data-type') === '' ? 'true' : 'false'); });
      filterPubs();
    }
    var d = t.closest('details');
    if (d) d.open = true;
  }
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest('a[href^="#"]');
    if (a && a.getAttribute('href').length > 1) revealTarget(a.getAttribute('href').slice(1));
  });
  if (location.hash.length > 1) revealTarget(location.hash.slice(1));

  /* upcoming events */
  var today = new Date(); today.setHours(0, 0, 0, 0);
  var upcoming = [];
  Array.prototype.forEach.call(document.querySelectorAll('.talk[data-date]'), function (li) {
    var parts = li.getAttribute('data-date').split('-').map(Number);
    if (parts.length < 3) return;
    var d = new Date(parts[0], parts[1] - 1, parts[2]);
    if (d >= today) {
      var badge = document.createElement('span');
      badge.className = 'badge';
      badge.textContent = 'Upcoming';
      li.querySelector('.t-type').appendChild(badge);
      upcoming.push({ el: li, date: d });
    }
  });
  var next = document.getElementById('hero-next');
  if (next && upcoming.length) {
    upcoming.sort(function (x, y) { return x.date - y.date; });
    var u = upcoming[0].el;
    var strong = document.createElement('strong');
    strong.textContent = 'Next: ';
    next.appendChild(strong);
    var link = document.createElement('a');
    link.href = '#' + u.id;
    link.textContent = u.getAttribute('data-title');
    next.appendChild(link);
    next.appendChild(document.createTextNode('. ' + u.getAttribute('data-detail') + ', ' + u.querySelector('.t-date').textContent + '.'));
    next.hidden = false;
  }

  /* header state and section highlighting */
  var header = document.querySelector('.site-header');
  function onScroll() { if (header) header.classList.toggle('is-scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  var navLinks = Array.prototype.slice.call(document.querySelectorAll('.site-nav a'));
  if ('IntersectionObserver' in window) {
    var byId = {};
    navLinks.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        navLinks.forEach(function (a) { a.removeAttribute('aria-current'); });
        var a = byId[en.target.id];
        if (a) a.setAttribute('aria-current', 'true');
      });
    }, { rootMargin: '-35% 0px -60% 0px' });
    Object.keys(byId).forEach(function (id) { var s = document.getElementById(id); if (s) io.observe(s); });
    var heroSec = document.getElementById('top'); if (heroSec) io.observe(heroSec);
  }

  /* print everything */
  window.addEventListener('beforeprint', function () {
    Array.prototype.forEach.call(document.querySelectorAll('details'), function (d) { d.open = true; });
  });
})();
"""

# ================================================================ page
def build_jsonld():
    pid = SITE_URL + "#person"
    graph = [
        {"@type": "WebSite", "@id": SITE_URL + "#website", "url": SITE_URL, "name": "Dr Farah Nadeem",
         "inLanguage": "en-GB", "publisher": {"@id": pid}},
        {"@type": "ProfilePage", "@id": SITE_URL + "#page", "url": SITE_URL, "name": TITLE,
         "description": DESCRIPTION, "isPartOf": {"@id": SITE_URL + "#website"}, "inLanguage": "en-GB",
         "dateModified": UPDATED, "mainEntity": {"@id": pid}, "about": {"@id": pid}},
        {"@type": "Person", "@id": pid, "name": "Farah Nadeem", "givenName": "Farah", "familyName": "Nadeem",
         "honorificPrefix": "Dr", "honorificSuffix": "PhD", "jobTitle": "Assistant Professor",
         "description": BIO_SHORT, "url": SITE_URL, "email": "mailto:" + EMAIL,
         "image": SITE_URL + "farah-nadeem.jpg",
         "identifier": {"@type": "PropertyValue", "propertyID": "ORCID", "value": ORCID_ID, "url": "https://orcid.org/" + ORCID_ID},
         "worksFor": {"@type": "CollegeOrUniversity", "name": "Lahore University of Management Sciences (LUMS)",
                      "url": "https://lums.edu.pk/",
                      "department": {"@type": "Organization",
                                     "name": "Syed Ahsan Ali and Syed Maratib Ali School of Education",
                                     "url": "https://soe.lums.edu.pk/"}},
         "workLocation": {"@type": "Place", "name": "Lahore, Pakistan"},
         "alumniOf": [
             {"@type": "CollegeOrUniversity", "name": "University of Washington", "url": "https://www.washington.edu/"},
             {"@type": "CollegeOrUniversity", "name": "National University of Computer and Emerging Sciences (FAST-NUCES)"},
             {"@type": "CollegeOrUniversity", "name": "National University of Sciences and Technology (NUST)"}],
         "knowsAbout": KNOWS_ABOUT,
         "award": [a[1] + " (" + a[0] + ")" for a in AWARDS],
         "sameAs": [u for _, u in PROFILES]},
    ]
    for p in PUBS:
        authors = [{"@type": "Person", "name": n.strip()} for n in
                   p["authors"].replace(", and ", ", ").replace(" and ", ", ").split(",")]
        for a in authors:
            if a["name"] == "F. Nadeem":
                a.clear(); a["@id"] = pid
        item = {"name": p["title"], "author": authors, "datePublished": str(p["year"])}
        if p["type"] == "thesis":
            item.update({"@type": "Thesis", "inSupportOf": "PhD", "url": p["href"],
                         "sourceOrganization": {"@type": "CollegeOrUniversity", "name": "University of Washington"}})
        elif p.get("doi"):
            item.update({"@type": "ScholarlyArticle", "headline": p["title"], "url": p["href"],
                         "sameAs": "https://doi.org/" + p["doi"],
                         "publisher": {"@type": "Organization", "name": "Association for Computational Linguistics"}})
        elif p["type"] == "report":
            item.update({"@type": "Report"})
            if p.get("href"):
                item["url"] = p["href"]
        else:
            continue
        graph.append(item)
    graph.append({"@type": "BlogPosting", "headline": "The Digital Doorway: Bridging the Gap Between Observation and Support",
                  "datePublished": "2026-03-30", "url": DOORWAY,
                  "author": [{"@id": pid}, {"@type": "Person", "name": "Areej Mahmood"}, {"@type": "Person", "name": "Nighat Lone"}],
                  "publisher": {"@type": "Organization", "name": "Data and Research in Education Research Consortium (DARE-RC)"}})
    for p in PROJECTS:
        if p["kind"] != "Research":
            continue
        proj = {"@type": "ResearchProject", "name": p["title"], "description": p["desc"][0],
                "url": SITE_URL + "#" + p["id"], "member": {"@id": pid}}
        for k, v in p["meta"]:
            if k == "Funding":
                proj["funder"] = {"@type": "Organization", "name": v}
        graph.append(proj)
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


def photo_uri():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "portrait.webp")
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return "data:image/webp;base64," + base64.b64encode(f.read()).decode("ascii")


def build_html():
    counts = region_counts()
    regions_js = {k: {"label": v["label"], "text": v["text"]} for k, v in REGIONS.items()}
    js = JS.replace("/*REGIONS*/", json.dumps(regions_js, ensure_ascii=False))

    chips = "".join(chip_html(k) for k in CHIP_ORDER)
    projects = "".join(project_html(p) for p in PROJECTS)
    main_pubs = [p for p in PUBS if not p.get("earlier")]
    earlier_pubs = [p for p in PUBS if p.get("earlier")]
    pub_chips = "".join(
        f'<button type="button" class="chip" data-type="{k}" aria-pressed="{"true" if k == "" else "false"}">{e(lbl)}</button>'
        for k, lbl in PUB_TYPES)
    talks = "".join(talk_html(t) for t in TALKS)
    courses = "".join(f'<li><span class="what">{e(c)}</span><span class="meta">{e(m)}</span></li>' for c, m in COURSES)
    leadership = "".join(
        f'<li><span class="when">{e(w)}</span><span><span class="what">'
        f'{(f"<a href={chr(34)}{e(h)}{chr(34)}>{e(t)}</a>") if h else e(t)}</span></span></li>'
        for w, t, h in LEADERSHIP)
    experience = "".join(
        f'<li><span class="when">{e(w)}</span><span><span class="what">{e(r)}</span><span class="meta">{e(o)}</span>'
        f'{(f"<span class={chr(34)}meta{chr(34)}>{e(d)}</span>") if d else ""}</span></li>'
        for w, r, o, d in EXPERIENCE)
    education = "".join(
        f'<li><span class="when">{e(w)}</span><span><span class="what">{e(d)}</span><span class="meta">{e(i)}</span></span></li>'
        for w, d, i in EDUCATION)
    awards = "".join(
        f'<li><span class="when">{e(w)}</span><span><span class="what">'
        f'{(f"<a href={chr(34)}{e(h)}{chr(34)}>{e(t)}</a>") if h else e(t)}</span></span></li>'
        for w, t, h in AWARDS)
    profiles = "".join(f'<li><a href="{e(u)}">{e(n)}</a></li>' for n, u in PROFILES)
    bio = "".join(f"<p>{e(p)}</p>" for p in BIO_LONG)
    bio_long_text = " ".join(BIO_LONG)
    brand_glyph = glyph("abc", cls="glyph", labelled=False)
    og_image = SITE_URL + "og-image.png"
    uri = photo_uri()
    portrait = (f'<img class="portrait" src="{uri}" width="288" height="288" alt="Portrait of Farah Nadeem">' if uri else "")

    page = f"""<!doctype html>
<html lang="en-GB" class="no-js">
<head>
<meta charset="utf-8">
<script>try{{var t=localStorage.getItem('theme');if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(TITLE)}</title>
<meta name="description" content="{e(DESCRIPTION)}">
<meta name="author" content="Farah Nadeem">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{SITE_URL}">
<link rel="alternate" type="text/plain" href="{SITE_URL}llms.txt" title="Plain-text summary for AI tools">
<meta property="og:type" content="profile">
<meta property="og:site_name" content="Dr Farah Nadeem">
<meta property="og:title" content="{e(TITLE)}">
<meta property="og:description" content="{e(DESCRIPTION)}">
<meta property="og:url" content="{SITE_URL}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Farah Nadeem. Three overlapping circles: AI and data science, education systems and policy, equity and inclusion.">
<meta property="og:locale" content="en_GB">
<meta property="profile:first_name" content="Farah">
<meta property="profile:last_name" content="Nadeem">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(TITLE)}">
<meta name="twitter:description" content="{e(DESCRIPTION)}">
<meta name="twitter:image" content="{og_image}">
<meta name="theme-color" content="#F7F8F6" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0F1626" media="(prefers-color-scheme: dark)">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@200..800&amp;text=0123456789&amp;display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Next:ital,wght@0,200..800;1,200..800&amp;display=swap">
<script type="application/ld+json">
{build_jsonld()}
</script>
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="#top">{brand_glyph}<span>Farah Nadeem</span></a>
    <nav class="site-nav" aria-label="Sections">
      <ul>
        <li><a href="#research">Research</a></li>
        <li><a href="#publications">Publications</a></li>
        <li><a href="#writing">Writing and talks</a></li>
        <li><a href="#teaching">Teaching</a></li>
        <li><a href="#about">About</a></li>
        <li><a href="#contact">Contact</a></li>
      </ul>
    </nav>
    <button type="button" class="theme-toggle js-only" id="theme-toggle" aria-pressed="false" aria-label="Dark theme">{THEME_ICON}</button>
  </div>
</header>

<main id="main">
  <section class="wrap hero" id="top" aria-labelledby="hero-name">
    <div class="hero-text">
      {portrait}
      <h1 id="hero-name"><span>Farah</span> <span>Nadeem</span></h1>
      <p class="hero-role">Assistant Professor, School of Education, <abbr title="Lahore University of Management Sciences">LUMS</abbr>, Lahore</p>
      <p class="hero-statement">I bring machine learning and <span class="nw">large-scale</span> education data to questions of assessment, teaching and fair access to school, mostly in Pakistan.</p>
      <p class="hero-note js-only">My work sits where three fields meet. Select an area on the map to filter my projects.</p>
      <ul class="hero-links">
        <li><a href="mailto:{EMAIL}">Email me</a></li>
        <li><a href="{e(PROFILES[0][1])}">Google Scholar</a></li>
        <li><a href="{e(PROFILES[1][1])}">LinkedIn</a></li>
        <li><a href="{e(PROFILES[2][1])}">GitHub</a></li>
      </ul>
      <p class="hero-next" id="hero-next" hidden></p>
    </div>
    <figure class="venn-figure">
      {VENN}
      <figcaption class="venn-caption" id="venn-caption">The map shows the three fields my work connects and where they overlap. The centre holds work that draws on all three.</figcaption>
    </figure>
  </section>

  <section class="section" id="research" aria-labelledby="research-h">
    <div class="wrap">
      <div class="section-head">
        <h2 id="research-h">Research</h2>
        <p class="section-intro">Studies I lead or contribute to, with the papers, briefs, talks and code from each. The small map beside each project shows which of the three areas it draws on.</p>
      </div>
      <div class="filters indent js-only">
        <div role="group" aria-labelledby="area-label">
          <p class="control-label" id="area-label">Filter by area</p>
          <div class="chips">{chips}</div>
        </div>
        <p class="count" id="project-count" aria-live="polite"></p>
      </div>
      <div class="projects">{projects}</div>
    </div>
  </section>

  <section class="section band" id="publications" aria-labelledby="pubs-h">
    <div class="wrap">
      <div class="section-head">
        <h2 id="pubs-h">Publications</h2>
        <p class="section-intro">Peer-reviewed papers, conference presentations, reports and my doctoral thesis. Citation counts are on <a href="{e(PROFILES[0][1])}">Google Scholar</a>.</p>
      </div>
      <div class="pub-tools indent js-only">
        <div class="search-field">
          <label class="control-label" for="pub-search">Search publications</label>
          <input id="pub-search" type="search" placeholder="Title, co-author, venue or year" autocomplete="off" spellcheck="false">
        </div>
        <div role="group" aria-labelledby="type-label">
          <p class="control-label" id="type-label">Type</p>
          <div class="chips">{pub_chips}</div>
        </div>
        <p class="count" id="pub-count" aria-live="polite"></p>
      </div>
      <p class="empty indent" id="pub-empty" hidden>No publications match. Try a co-author's surname, or a venue such as BEA or AERA.</p>
      <div class="pubs">{pub_groups(main_pubs)}</div>
      <details class="earlier indent" id="earlier-work">
        <summary>Earlier research in wireless networking, 2014 to 2016</summary>
        <div class="pubs">{pub_groups(earlier_pubs)}</div>
      </details>
    </div>
  </section>

  <section class="section" id="writing" aria-labelledby="writing-h">
    <div class="wrap">
      <div class="section-head">
        <h2 id="writing-h">Writing and talks</h2>
        <p class="section-intro">Blog posts, talks, panels and podcasts, newest first.</p>
      </div>
      <ol class="talks">{talks}</ol>
    </div>
  </section>

  <section class="section band" id="teaching" aria-labelledby="teaching-h">
    <div class="wrap">
      <div class="section-head">
        <h2 id="teaching-h">Teaching and leadership</h2>
        <p class="section-intro">Graduate teaching at LUMS, professional workshops, and institutional and academic service.</p>
      </div>
      <div class="cols indent">
        <div>
          <h3>Courses</h3>
          <ul class="plain">{courses}</ul>
          <p class="note">{e(TEACHING_NOTE)}</p>
        </div>
        <div>
          <h3>Leadership and service</h3>
          <ul class="dated">{leadership}</ul>
          <p class="note">{e(REVIEWING)}</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section" id="about" aria-labelledby="about-h">
    <div class="wrap">
      <div class="section-head">
        <h2 id="about-h">About</h2>
        <div class="bio">{bio}</div>
      </div>
      <div class="copy-row indent js-only">
        <button type="button" class="small-btn" data-copy="{e(BIO_SHORT)}" data-done="Short bio copied">Copy short bio</button>
        <button type="button" class="small-btn" data-copy="{e(bio_long_text)}" data-done="Full bio copied">Copy full bio</button>
      </div>
      <div class="about-facts indent">
        <div>
          <h3>Experience</h3>
          <ul class="dated">{experience}</ul>
        </div>
        <div class="stack">
          <div><h3>Education</h3><ul class="dated">{education}</ul></div>
          <div><h3>Recognition</h3><ul class="dated">{awards}</ul></div>
          <div><h3>Methods</h3><p>{e(METHODS)}</p></div>
        </div>
      </div>
    </div>
  </section>

  <section class="section contact" id="contact" aria-labelledby="contact-h">
    <div class="wrap">
      <div class="section-head">
        <h2 id="contact-h">Contact</h2>
        <div>
          <p class="section-intro">Email is the best way to reach me about research, collaboration and speaking.</p>
          <a class="email-big" href="mailto:{EMAIL}">{EMAIL}</a>
          <p class="visually-hidden">Profiles</p>
          <ul class="profiles">{profiles}</ul>
        </div>
      </div>
      <footer class="site-footer">
        <p>School of Education, Lahore University of Management Sciences, Lahore, Pakistan.</p>
        <p>This site aims to meet WCAG 2.2 AA. If anything is hard to read or use, please email me. Last updated {UPDATED_LABEL}.</p>
      </footer>
    </div>
  </section>
</main>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script>{js}</script>
</body>
</html>
"""
    return page


def build_llms():
    lines = [
        "# Dr Farah Nadeem",
        "",
        "> Assistant Professor at the Syed Ahsan Ali and Syed Maratib Ali School of Education, Lahore University of "
        "Management Sciences (LUMS), Pakistan. Her research uses machine learning and large-scale education data to "
        "study assessment, teacher development and fair access to school.",
        "",
        "Disambiguation: this Farah Nadeem is an education and machine learning researcher at LUMS. She is a "
        "different person from the Pakistani actress of the same name.",
        "",
        "## Key facts",
        "",
        "- Current role: Assistant Professor, School of Education, LUMS, Lahore (since 2023)",
        "- Research areas: AI and data science; education systems and policy; equity and inclusion",
        "- Education: PhD in Electrical and Computer Engineering, University of Washington (2020), Fulbright Fellow; "
        "MS Electrical Engineering, FAST-NUCES (2014); BS Electrical Engineering, NUST (2008)",
        "- Previous roles: Director, Office of Accessibility and Inclusion, LUMS (2023 to 2025); Education Consultant, "
        "World Bank Education Global Practice (2023 to 2025); Education Technology and MIS Expert, UNICEF Pakistan "
        "(2021 to 2023); Monitoring and Evaluation Specialist, PMIU, Punjab Education Sector Reforms Programme (2020 to 2021)",
        f"- Website: {SITE_URL}",
        f"- ORCID: https://orcid.org/{ORCID_ID}",
        f"- Email: {EMAIL}",
        "",
        "## Bio",
        "",
        " ".join(BIO_LONG),
        "",
        "## Research projects",
        "",
    ]
    for p in PROJECTS:
        meta = "; ".join(f"{k}: {v}" for k, v in p["meta"])
        areas = ", ".join(AREAS[k]["name"] for k in "abc" if k in p["areas"])
        lines.append(f"- [{p['title']}]({SITE_URL}#{p['id']}) ({p['when']}; {p['kind'].lower()}). {meta}. "
                     f"Areas: {areas}. {p['desc'][0]}")
    lines += ["", "## Publications", ""]
    for p in PUBS:
        url = p.get("href") or (p["links"][0][1] if p.get("links") else SITE_URL + "#" + p["id"])
        lines.append(f"- [{p['title']}]({url}): {p['authors']}. {p['venue']}.")
    lines += ["", "## Writing and talks", ""]
    for t in TALKS:
        url = t.get("href") or SITE_URL + "#" + t["id"]
        lines.append(f"- {t['label']}, {t['type']}: [{t['title']}]({url}). {t['detail']}.")
    lines += ["", "## Teaching", ""]
    for c, m in COURSES:
        lines.append(f"- {c} ({m.lower()})")
    lines += ["", "## Recognition", ""]
    for w, t, _ in AWARDS:
        lines.append(f"- {t} ({w})")
    lines += ["", "## Profiles", ""]
    for n, u in PROFILES:
        lines.append(f"- [{n}]({u})")
    lines.append("")
    return "\n".join(lines)


ROBOTS = f"""# Search engines and AI assistants are welcome to read this site.
User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: Claude-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

Sitemap: {SITE_URL}sitemap.xml
"""

SITEMAP = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{SITE_URL}</loc>
    <lastmod>{UPDATED}</lastmod>
  </url>
</urlset>
"""


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.dirname(here) if os.path.basename(here) == "source" else here
    files = {"index.html": build_html(), "llms.txt": build_llms(), "robots.txt": ROBOTS, "sitemap.xml": SITEMAP}
    for name, text in files.items():
        with open(os.path.join(out, name), "w", encoding="utf-8") as f:
            f.write(text)
        print("wrote", os.path.join(out, name))

"""
Demo data for EDUDESK.

IMPORTANT: every record here is DEMO data. Names and official websites point to real
organisations so students can verify details, but amounts, dates, fees and eligibility
are intentionally general or left as "verify on the official website".

Run manually (optional - the app seeds itself on first start):
    python database/seed.py            # add demo data if the database is empty
    python database/seed.py --reset    # delete everything and re-create the demo data
    python database/seed.py --aktu     # reload only the AKTU 1st-year study material (keeps users/applications)
"""
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # so "import models" works when run directly

from models import AktuSubject, AktuUnit, College, Deadline, Exam, Scholarship, Service, db   # noqa: E402

VERIFY = "Varies every year — verify on the official website."
APPLY_STEPS = [
    "Read the official notification and confirm you are eligible",
    "Collect the required documents (scan them clearly)",
    "Register on the official website with your own email and mobile number",
    "Fill the form carefully and upload documents in the requested size and format",
    "Submit, save the acknowledgement or application number, and note the last date",
    "Add it to your EDUDESK tracker and update the status as you go",
]

SERVICES = [
    ("Scholarship Application Guidance", "Scholarships",
     "Step-by-step help to find a scholarship you qualify for, prepare documents and submit the application correctly.",
     "Depends on the scheme: usually marks, family income, category, course and state.",
     ["Aadhaar / photo ID", "Previous marksheet", "Income certificate (if required)", "Category certificate (if required)", "Bank passbook", "Passport-size photo"],
     APPLY_STEPS, "https://scholarships.gov.in", "Get help choosing and applying for a scholarship"),
    ("National Scholarship Portal (NSP) Registration Help", "Scholarships",
     "Understand how to register and apply on the National Scholarship Portal, a central website where many scholarship schemes are listed.",
     "Each scheme on the portal has its own eligibility. Check the scheme page.",
     ["Aadhaar details", "Mobile number linked to Aadhaar (if asked)", "Bank account details", "Institute details", "Income / category certificates as required"],
     ["Open the official portal and read the instructions", "Complete one-time registration", "Log in and choose the scheme you are eligible for",
      "Fill details and upload documents", "Submit and note the application ID", "Follow up with your institute for verification if the scheme requires it"],
     "https://scholarships.gov.in", "Help with NSP registration and application"),
    ("B.Tech Admission Process Guide", "College Admissions",
     "Understand the route to B.Tech: entrance exam, counselling, choice filling, document verification and fee payment.",
     "Usually 12th with Physics and Mathematics plus an accepted entrance exam. Rules differ by college.",
     ["Class 10 and 12 marksheets", "Entrance exam scorecard", "Category certificate (if applicable)", "Photo ID", "Passport-size photos", "Transfer / migration certificate"],
     ["Shortlist colleges and note the exam each accepts", "Register and appear for the entrance exam", "Register for counselling after results",
      "Fill and lock your college and branch choices", "Complete document verification", "Pay the seat acceptance fee and report to the college"],
     "https://josaa.nic.in", "Help with B.Tech admission steps"),
    ("Central University Admission (CUET)", "College Admissions",
     "Learn how admission to many central and participating universities works through a common entrance test.",
     "Depends on the course and university. Check each university's eligibility.",
     ["Class 12 marksheet or admit card", "Photo ID", "Photograph and signature", "Category certificate (if applicable)"],
     APPLY_STEPS, "https://cuet.nta.nic.in", "Help with university admission through CUET"),
    ("JEE Main Form Filling Help", "Entrance Exams",
     "Get guidance on filling the JEE Main application: personal details, exam centre choices, photo/signature upload and fee payment.",
     "Qualifying exam and attempt limits are listed in the Information Bulletin.",
     ["Class 10 certificate", "Class 12 details", "Photograph and signature", "Photo ID", "Category / EWS / PwD certificate (if applicable)"],
     APPLY_STEPS, "https://jeemain.nta.nic.in", "Help filling the JEE Main form"),
    ("NEET UG Form Filling Help", "Entrance Exams",
     "Guidance for the NEET UG application: details, documents, photo/signature upload, and fee payment.",
     "Qualifying subjects, age and attempt rules are in the official bulletin.",
     ["Class 10 certificate", "Class 12 details", "Photograph and signature", "Photo ID", "Category / PwD certificate (if applicable)"],
     APPLY_STEPS, "https://neet.nta.nic.in", "Help filling the NEET UG form"),
    ("SSC Exam Application Help", "Competitive Exams",
     "Understand One-Time Registration and how to apply for Staff Selection Commission exams.",
     "Each exam has its own age and qualification rules in its notice.",
     ["Photo ID", "Educational certificates", "Photograph and signature", "Category certificate (if applicable)"],
     APPLY_STEPS, "https://ssc.gov.in", "Help applying for an SSC exam"),
    ("UPSC Civil Services Application Help", "Competitive Exams",
     "Learn how to apply for UPSC examinations, including one-time registration and the application steps.",
     "Degree, age and attempt limits are in the official notification.",
     ["Photo ID", "Graduation proof", "Photograph and signature", "Category certificate (if applicable)"],
     APPLY_STEPS, "https://upsc.gov.in", "Help applying for UPSC"),
    ("State Education Scheme Guidance", "Government Education Schemes",
     "Find out how to look for scholarships and fee-benefit schemes run by your own state government.",
     "Usually based on state domicile, category and income. Check your state's portal.",
     ["Domicile certificate", "Income certificate", "Category certificate", "Previous marksheet", "Bank passbook"],
     ["Search for your state's scholarship / education portal", "Read the scheme list and eligibility", "Register and apply before the portal closes", "Get your institute to verify if required"],
     "https://scholarships.gov.in", "Help finding state education schemes"),
    ("Income Certificate Help", "Certificates",
     "Understand how to apply for an income certificate, often needed for scholarships and fee benefits.",
     "Issued by your state government. Rules and validity differ by state.",
     ["Aadhaar", "Address proof", "Self-declaration / affidavit", "Salary slip or other income proof (if available)"],
     ["Find your state's online service portal or nearest service centre", "Check the document list for your state", "Submit the application with documents", "Download the certificate once approved and keep copies"],
     "https://services.india.gov.in", "Help applying for an income certificate"),
    ("Caste & Domicile Certificate Help", "Certificates",
     "Guidance on applying for caste and domicile (residence) certificates for scholarships and admissions.",
     "Issued by your state government. Check local rules.",
     ["Aadhaar", "Address proof", "Parent's certificate or relevant records", "Self-declaration / affidavit"],
     ["Find your state's service portal or nearest service centre", "Check the document list", "Submit the application", "Download and keep several copies"],
     "https://services.india.gov.in", "Help applying for caste or domicile certificate"),
    ("Photo, Signature & PDF Preparation", "Document Services",
     "Resize photos and signatures, compress images, and merge or split PDFs so your documents meet the form's requirements. Works inside your browser.",
     "Anyone filling an online form.",
     ["Your photo and signature images", "Scanned certificates"],
     ["Open the Document Center", "Check the size and format required by the form", "Resize or compress your file", "Download and upload it to the form"],
     None, "Help preparing photo, signature and PDFs"),
    ("DigiLocker Setup Help", "Document Services",
     "Learn to create a DigiLocker account to store and share digital copies of documents issued by participating organisations.",
     "Anyone with an Aadhaar-linked mobile number.",
     ["Mobile number", "Aadhaar number"],
     ["Open the official DigiLocker site or app", "Sign up with your mobile number", "Link Aadhaar and pull available documents", "Use 'issued documents' while applying where accepted"],
     "https://www.digilocker.gov.in", "Help setting up DigiLocker"),
    ("Internship Search Guidance", "Internships",
     "Find internships, prepare a short resume and understand how to apply safely.",
     "Open to students; each internship lists its own requirements.",
     ["Resume", "College ID", "Recent marksheet"],
     ["Create a one-page resume", "Check official internship portals and company career pages", "Apply to several, early", "Never pay money to get an internship offer"],
     "https://internship.aicte-india.org", "Help finding an internship"),
    ("Career Options After 12th", "Career Guidance",
     "Explore course and career options by stream, with the entrance exams you may need.",
     "Open to all students.",
     ["Class 10 and 12 marksheets (for later steps)"],
     ["Write down your interests and strengths", "Pick two or three streams or courses", "Check entrance exams and colleges in EDUDESK", "Talk to a counsellor and compare scholarships"],
     "https://www.ncs.gov.in", "Help choosing a career path"),
    ("Free Online Courses (SWAYAM)", "Courses",
     "Find free online courses from Indian institutions to build skills alongside your degree.",
     "Open to learners; certificates may need an exam fee.",
     ["Email ID", "Mobile number"],
     ["Open the SWAYAM website", "Create a free account", "Pick a course and enrol", "Note exam dates if you want a certificate"],
     "https://swayam.gov.in", "Help choosing an online course"),
    ("Education Loan Guidance", "Education Loans",
     "Understand how education loans work and how to compare banks through the Vidya Lakshmi portal.",
     "Depends on the bank, course and institute. Check each bank's rules.",
     ["Admission letter", "Fee structure", "Student KYC", "Marksheets", "Co-applicant income proof"],
     ["Keep admission and fee documents ready", "Compare interest rate and repayment rules", "Apply through the portal or the bank branch", "Track the loan status with the bank"],
     "https://www.vidyalakshmi.co.in", "Help with an education loan"),
    ("Career & Admission Counselling", "Counselling",
     "Talk to the EDUDESK assistance team on WhatsApp to clear doubts about courses, colleges and applications.",
     "Open to all students.",
     ["None needed to start"],
     ["Tap 'Need Help?'", "Send the pre-filled WhatsApp message", "Share your class, interests and questions"],
     None, "Talk to someone about your options"),
]

SCHOLARSHIPS = [
    # name, provider, type, eligibility text, documents, url, courses, levels, states, categories, max_income, min_marks
    ("Central Sector Scheme of Scholarships for College and University Students", "Ministry of Education, Government of India", "Government",
     "Merit-based support for college students. Demo criteria only.", ["Class 12 marksheet", "Income certificate", "Bank passbook", "Aadhaar"],
     "https://scholarships.gov.in", ["Any"], ["Undergraduate"], ["All India"], ["All"], 800000, 80),
    ("Post Matric Scholarship (Central Schemes on NSP)", "Government of India — via National Scholarship Portal", "Government",
     "Category-based support for post-matric students. Demo criteria only.", ["Category certificate", "Income certificate", "Previous marksheet", "Bank passbook", "Aadhaar"],
     "https://scholarships.gov.in", ["Any"], ["12th", "Undergraduate", "Postgraduate"], ["All India"], ["SC", "ST", "OBC"], 250000, None),
    ("AICTE Pragati Scholarship for Girls", "AICTE", "Government",
     "For girl students in AICTE-approved technical programmes. Demo criteria only.", ["Admission proof", "Income certificate", "Class 12 marksheet", "Aadhaar", "Bank passbook"],
     "https://www.aicte-india.org", ["B.Tech", "Diploma"], ["Undergraduate"], ["All India"], ["All"], 800000, None),
    ("AICTE Saksham Scholarship for Specially-Abled Students", "AICTE", "Government",
     "For students with disability in AICTE-approved technical programmes. Demo criteria only.", ["Disability certificate", "Admission proof", "Income certificate", "Aadhaar", "Bank passbook"],
     "https://www.aicte-india.org", ["B.Tech", "Diploma"], ["Undergraduate"], ["All India"], ["All"], 800000, None),
    ("INSPIRE Scholarship (Science)", "Department of Science and Technology", "Government",
     "For high-performing students pursuing natural and basic sciences. Demo criteria only.", ["Class 12 marksheet", "Admission proof", "Aadhaar", "Bank passbook"],
     "https://online-inspire.gov.in", ["B.Sc", "Integrated M.Sc"], ["Undergraduate"], ["All India"], ["All"], None, 85),
    ("Uttar Pradesh Post Matric Scholarship", "Government of Uttar Pradesh", "Government",
     "State scheme for eligible students of Uttar Pradesh. Demo criteria only.", ["Domicile certificate", "Income certificate", "Category certificate", "Previous marksheet", "Bank passbook"],
     "https://scholarship.up.gov.in", ["Any"], ["12th", "Undergraduate", "Postgraduate"], ["Uttar Pradesh"], ["All"], 200000, None),
    ("Reliance Foundation Undergraduate Scholarships", "Reliance Foundation", "Private",
     "Private merit-and-means scholarship for undergraduates. Demo criteria only.", ["Class 12 marksheet", "Income proof", "Admission proof", "Aadhaar"],
     "https://scholarships.reliancefoundation.org", ["Any"], ["Undergraduate"], ["All India"], ["All"], 1500000, 60),
    ("Tata Capital Pankh Scholarship", "Tata Capital", "Private",
     "Private scholarship for students from Class 11 onwards. Demo criteria only.", ["Previous marksheet", "Income proof", "Admission proof", "Aadhaar"],
     "https://www.buddy4study.com", ["Any"], ["12th", "Undergraduate"], ["All India"], ["All"], 400000, 60),
    ("Private Scholarship Listings on Buddy4Study", "Buddy4Study (listing website)", "Private",
     "A website that lists many private and government scholarships. Use it to discover more options.", ["Depends on the scholarship"],
     "https://www.buddy4study.com", ["Any"], ["10th", "12th", "Undergraduate", "Postgraduate"], ["All India"], ["All"], None, None),
    ("State Merit Scholarship Search (State Portals)", "State Governments", "Government",
     "Most states run their own merit and means scholarships. Search your state's portal.", ["Domicile certificate", "Income certificate", "Previous marksheet"],
     "https://scholarships.gov.in", ["Any"], ["10th", "12th", "Undergraduate"], ["All India"], ["All"], 300000, 60),
]

COLLEGES = [
    # name, city, state, type, courses, exams, fee_band, eligibility, admission, url
    ("IIT Bombay", "Mumbai", "Maharashtra", "Government", ["B.Tech", "M.Tech", "B.Des"], ["JEE Advanced", "JEE Main"], "Medium",
     "Qualifying exam and entrance score as per the current brochure.", "Entrance exam, then central counselling (JoSAA).", "https://www.iitb.ac.in"),
    ("IIT Kanpur", "Kanpur", "Uttar Pradesh", "Government", ["B.Tech", "M.Tech", "B.Sc"], ["JEE Advanced", "JEE Main"], "Medium",
     "Qualifying exam and entrance score as per the current brochure.", "Entrance exam, then central counselling (JoSAA).", "https://www.iitk.ac.in"),
    ("NIT Tiruchirappalli", "Tiruchirappalli", "Tamil Nadu", "Government", ["B.Tech", "M.Tech", "B.Arch"], ["JEE Main"], "Low",
     "Qualifying exam and JEE Main score as per the current rules.", "JEE Main, then central counselling (JoSAA).", "https://www.nitt.edu"),
    ("IIIT Allahabad", "Prayagraj", "Uttar Pradesh", "Government", ["B.Tech", "M.Tech"], ["JEE Main"], "Medium",
     "Qualifying exam and JEE Main score as per the current rules.", "JEE Main, then central counselling (JoSAA).", "https://www.iiita.ac.in"),
    ("University of Delhi", "New Delhi", "Delhi", "Government", ["B.A.", "B.Com", "B.Sc"], ["CUET"], "Low",
     "Depends on the course; see the current admission bulletin.", "CUET score, then university seat allocation.", "https://www.du.ac.in"),
    ("Banaras Hindu University", "Varanasi", "Uttar Pradesh", "Government", ["B.A.", "B.Sc", "B.Com", "B.Tech"], ["CUET", "JEE Main"], "Low",
     "Depends on the course; see the current admission bulletin.", "Entrance exam based; follow the university bulletin.", "https://www.bhu.ac.in"),
    ("AIIMS New Delhi", "New Delhi", "Delhi", "Government", ["MBBS"], ["NEET UG"], "Low",
     "NEET UG qualification and other rules in the official notice.", "NEET UG score, then medical counselling.", "https://www.aiims.edu"),
    ("Jadavpur University", "Kolkata", "West Bengal", "Government", ["B.Tech", "B.A.", "B.Sc"], ["WBJEE", "JEE Main"], "Low",
     "Depends on the course; see the official prospectus.", "Entrance exam or merit based, as stated in the prospectus.", "https://jadavpuruniversity.in"),
    ("Vellore Institute of Technology", "Vellore", "Tamil Nadu", "Private", ["B.Tech", "M.Tech", "BBA"], ["VITEEE"], "High",
     "See the official admission page for the current year.", "University entrance exam and counselling.", "https://vit.ac.in"),
    ("BITS Pilani", "Pilani", "Rajasthan", "Private", ["B.E.", "M.E.", "B.Pharm"], ["BITSAT"], "High",
     "See the official admission page for the current year.", "BITSAT score and institute counselling.", "https://www.bits-pilani.ac.in"),
    ("Manipal Academy of Higher Education", "Manipal", "Karnataka", "Private", ["B.Tech", "MBBS", "BBA"], ["MET", "NEET UG"], "High",
     "Depends on the programme; see the official site.", "Entrance exam or national exam score, then counselling.", "https://manipal.edu"),
    ("College of Engineering Pune", "Pune", "Maharashtra", "Government", ["B.Tech", "M.Tech"], ["MHT CET", "JEE Main"], "Low",
     "Qualifying exam and entrance score as per the current rules.", "State centralised admission process.", "https://www.coep.org.in"),
]

EXAMS = [
    # name, category, description, eligibility, registration, documents, url
    ("JEE Main", "Engineering", "National-level entrance exam for engineering and architecture programmes.",
     "Qualifying exam rules are in the Information Bulletin.", "Register online on the official website, fill the form, upload photo and signature, pay the fee.",
     ["Class 10 certificate", "Photo ID", "Photograph", "Signature", "Category certificate (if applicable)"], "https://jeemain.nta.nic.in"),
    ("JEE Advanced", "Engineering", "Exam for admission to the IITs for those who qualify through JEE Main.",
     "Only students who meet the official criteria can register.", "Registration on the official website after qualifying; follow the current brochure.",
     ["JEE Main details", "Class 10 / 12 documents", "Photograph", "Category certificate (if applicable)"], "https://jeeadv.ac.in"),
    ("BITSAT", "Engineering", "Admission test for BITS campuses.",
     "See the official admission page.", "Register online on the official admission site.",
     ["Class 12 details", "Photograph", "Signature", "Photo ID"], "https://www.bitsadmission.com"),
    ("NEET UG", "Medical", "National entrance test for MBBS, BDS and related medical courses.",
     "Qualifying subjects and age rules are in the official bulletin.", "Register on the official website, upload documents, pay fee, download the admit card.",
     ["Class 10 certificate", "Photo ID", "Photograph", "Signature", "Category certificate (if applicable)"], "https://neet.nta.nic.in"),
    ("CUET (UG)", "University Entrance", "Common test for admission to many central and participating universities.",
     "Check the university you want to apply to.", "Register on the official site, choose subjects and universities, pay fee.",
     ["Class 12 details", "Photo ID", "Photograph", "Signature", "Category certificate (if applicable)"], "https://cuet.nta.nic.in"),
    ("CLAT", "University Entrance", "Common law entrance test for National Law Universities.",
     "See the official consortium website.", "Register online on the official site and pay the fee.",
     ["Class 12 details", "Photo ID", "Photograph", "Signature", "Category certificate (if applicable)"], "https://consortiumofnlus.ac.in"),
    ("UPSC Civil Services Examination", "Government Exams", "Exam for recruitment to central civil services.",
     "Degree, age and attempts are in the official notification.", "One-time registration, then the online application when the notice is released.",
     ["Photo ID", "Graduation proof", "Photograph", "Signature", "Category certificate (if applicable)"], "https://upsc.gov.in"),
    ("SSC Combined Graduate Level (CGL)", "Government Exams", "Recruitment exam for various central government posts.",
     "Check the official notice for the current year.", "One-time registration, then apply when the notice is released.",
     ["Photo ID", "Educational certificates", "Photograph", "Signature"], "https://ssc.gov.in"),
    ("CAT", "Competitive Exams", "Common admission test for management programmes at IIMs and other institutes.",
     "Graduation requirement and rules are in the official notice.", "Register online on the official website and pay the fee.",
     ["Graduation details", "Photo ID", "Photograph", "Category certificate (if applicable)"], "https://iimcat.ac.in"),
    ("IBPS Banking Exams", "Competitive Exams", "Recruitment exams for public sector banks.",
     "Check the official notice for the current year.", "Register on the official site when the notification is released.",
     ["Photo ID", "Educational certificates", "Photograph", "Signature", "Thumb impression"], "https://www.ibps.in"),
]

# (title, category, days from today, description, url)
DEADLINES = [
    ("Sample: Scholarship portal application window closes", "Scholarships", 3, "Example reminder to show how EDUDESK warns you before a closing date.", "https://scholarships.gov.in"),
    ("Sample: Entrance exam form last date", "Entrance Exams", 6, "Example reminder. Real dates are published in the official notification.", "https://jeemain.nta.nic.in"),
    ("Sample: Document verification slot", "College Admissions", 12, "Example reminder for a counselling step.", "https://josaa.nic.in"),
    ("Sample: Education loan document submission", "Education Loans", 20, "Example reminder to submit papers to a bank.", "https://www.vidyalakshmi.co.in"),
    ("Sample: University admission form closes", "College Admissions", 33, "Example reminder for a university application.", "https://cuet.nta.nic.in"),
    ("Sample: Government exam registration ends", "Competitive Exams", 45, "Example reminder for a government exam form.", "https://ssc.gov.in"),
    ("Sample: Scholarship renewal reminder (passed)", "Scholarships", -8, "Example of a deadline that has already passed.", "https://scholarships.gov.in"),
    ("Sample: Counselling registration (passed)", "Counselling", -25, "Example of a past deadline.", "https://josaa.nic.in"),
]


def seed_all(reset=False):
    """Insert demo data. Call inside an app context."""
    if reset:
        db.drop_all()
    db.create_all()
    for title, category, description, eligibility, documents, steps, url, help_note in SERVICES:
        db.session.add(Service(title=title, category=category, description=description, eligibility=eligibility,
                               documents=documents, steps=steps, important_dates=VERIFY, official_url=url, assistance_note=help_note))
    for (name, provider, kind, eligibility, documents, url, courses, levels, states, categories, max_income, min_marks) in SCHOLARSHIPS:
        db.session.add(Scholarship(name=name, provider=provider, type=kind, eligibility=eligibility, description=eligibility,
                                   documents=documents, official_url=url, courses=courses, levels=levels, states=states,
                                   categories=categories, max_income=max_income, min_marks=min_marks,
                                   benefit="Varies — check the official notification", last_date="Check official notification"))
    for name, city, state, kind, courses, exams, fee_band, eligibility, admission, url in COLLEGES:
        db.session.add(College(name=name, city=city, state=state, type=kind, courses=courses, entrance_exams=exams,
                               fee_band=fee_band, eligibility=eligibility, admission_process=admission, official_url=url,
                               description=f"{kind} institution in {city}, {state}."))
    for name, category, description, eligibility, registration, documents, url in EXAMS:
        db.session.add(Exam(name=name, category=category, description=description, eligibility=eligibility,
                            registration_process=registration, documents=documents, official_url=url,
                            important_dates="Check the official notification for current dates."))
    today = date.today()
    for title, category, offset, description, url in DEADLINES:
        db.session.add(Deadline(title=title, category=category, date=today + timedelta(days=offset), description=description,
                                official_url=url, is_verified=False, source_label="Demo data — not a real deadline"))
    db.session.commit()
    seed_aktu()
    print("Demo data loaded.")


def seed_aktu():
    """Load the AKTU first-year study content (syllabus, notes, questions). Safe to call on an existing database."""
    from models import AktuSubject, AktuUnit
    from database.aktu_content import all_subjects
    db.create_all()
    for order, item in enumerate(all_subjects(), start=1):
        subject = AktuSubject(code=item["code"], alt_code=item.get("alt_code"), name=item["name"], category=item["category"],
                              credits=item["credits"], ltp=item["ltp"], objective=item.get("objective", ""), syllabus_note=item.get("note", ""),
                              books=item.get("books", []), labs=item.get("labs", []), sort_order=order)
        for unit in item["units"]:
            subject.units.append(AktuUnit(number=unit["number"], title=unit["title"], hours=unit["hours"],
                                          syllabus=unit["syllabus"], notes=unit["notes"], questions=unit["questions"]))
        db.session.add(subject)
    db.session.commit()
    print("AKTU study content loaded.")


if __name__ == "__main__":
    from app import app          # importing the app also creates the tables
    with app.app_context():
        if "--aktu" in sys.argv:
            seed_aktu()          # only (re)load the AKTU study material, keeps users and applications
        elif "--reset" in sys.argv:
            seed_all(reset=True)
        elif Service.query.count() == 0:
            seed_all()
        else:
            print("Database already has data. Use --reset to start over.")

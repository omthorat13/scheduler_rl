"""
Generates the OSDS Course Project Report in .docx format,
matching the VIT template's formatting style exactly:
  - All paragraphs use 'Normal' style (NO Heading styles)
  - Section titles are manually bold + larger font size + centered
  - Body text is justified
  - Font: Times New Roman throughout
"""
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(BASE_DIR, "OSDS_Project_Report.docx")
COMPARISON_IMG = os.path.join(BASE_DIR, "results", "comparison.png")

FONT_NAME = "Times New Roman"


def set_cell_shading(cell, color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), color)
    shading.set(qn('w:val'), 'clear')
    tcPr.append(shading)


def add_empty_para(doc, size=6):
    p = doc.add_paragraph()
    run = p.add_run("")
    run.font.size = Pt(size)
    run.font.name = FONT_NAME
    return p


def add_para(doc, text, bold=False, italic=False, size=12,
             alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, space_before=0):
    p = doc.add_paragraph()
    p.alignment = alignment
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.name = FONT_NAME
    return p


def add_center(doc, text, bold=False, size=12, space_after=4, space_before=0):
    return add_para(doc, text, bold=bold, size=size,
                    alignment=WD_ALIGN_PARAGRAPH.CENTER,
                    space_after=space_after, space_before=space_before)


def add_section_title(doc, text, size=15, space_before=12, space_after=8):
    """Mimics template's section headings: bold, larger font, centered."""
    return add_center(doc, text, bold=True, size=size,
                      space_after=space_after, space_before=space_before)


def add_subsection_title(doc, text, size=13, space_before=10, space_after=6):
    return add_para(doc, text, bold=True, size=size,
                    alignment=WD_ALIGN_PARAGRAPH.LEFT,
                    space_after=space_after, space_before=space_before)


def add_bullet(doc, text, bold_prefix=None, size=11):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(3)
    if bold_prefix:
        run = p.add_run(bold_prefix)
        run.bold = True
        run.font.size = Pt(size)
        run.font.name = FONT_NAME
        run = p.add_run(text)
        run.font.size = Pt(size)
        run.font.name = FONT_NAME
    else:
        run = p.add_run(text)
        run.font.size = Pt(size)
        run.font.name = FONT_NAME
    return p


def make_table(doc, headers, rows, col_widths=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Header row
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ""
        para = cell.paragraphs[0]
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.add_run(h)
        run.bold = True
        run.font.size = Pt(10)
        run.font.name = FONT_NAME
        set_cell_shading(cell, 'D9E2F3')
    # Data rows
    for r, row_data in enumerate(rows):
        for c, val in enumerate(row_data):
            cell = table.rows[r + 1].cells[c]
            cell.text = ""
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = para.add_run(str(val))
            run.font.size = Pt(10)
            run.font.name = FONT_NAME
    if col_widths:
        for i, w in enumerate(col_widths):
            for row in table.rows:
                row.cells[i].width = Cm(w)
    return table


def build_report():
    doc = Document()

    # ===== Set default style =====
    style = doc.styles['Normal']
    style.font.name = FONT_NAME
    style.font.size = Pt(12)
    style.paragraph_format.space_after = Pt(6)
    style.paragraph_format.line_spacing = 1.15

    # Also set the rFonts for East Asian / other scripts
    rPr = style.element.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), FONT_NAME)
    rFonts.set(qn('w:hAnsi'), FONT_NAME)
    rFonts.set(qn('w:cs'), FONT_NAME)
    rPr.append(rFonts)

    # ===========================================================================
    # COVER PAGE
    # ===========================================================================
    add_empty_para(doc, 12)
    add_center(doc, "OPERATING SYSTEMS AND DISTRIBUTED SYSTEMS", bold=True, size=16, space_after=6)
    add_center(doc, "Course Project Report on", bold=True, size=14, space_after=6)
    add_center(doc, "\u201cML-Based CPU Scheduler: Direct Policy Learning\nwith Reinforcement Learning\u201d",
               bold=True, size=16, space_after=6)
    add_center(doc, "A DQN Agent for Intelligent Process Dispatch in Operating Systems",
               bold=True, size=13, space_after=16)

    add_center(doc, "SUBMITTED IN PARTIAL FULFILLMENT OF THE REQUIREMENTS FOR", size=11, space_after=0)
    add_center(doc, "THE DEGREE OF", size=11, space_after=6)
    add_center(doc, "BACHELOR OF TECHNOLOGY IN", bold=True, size=12, space_after=2)
    add_center(doc, "Department of CSE - IOTCSBT", bold=True, size=12, space_after=2)
    add_center(doc, "OF", bold=True, size=12, space_after=2)
    add_center(doc, "VISHWAKARMA INSTITUTE OF TECHNOLOGY", bold=True, size=14, space_after=2)
    add_center(doc, "Savitribai Phule Pune University", bold=True, size=14, space_after=16)

    add_center(doc, "SHARAD SHINDE (12412393)", bold=True, size=12, space_after=2)
    add_center(doc, "YASH WAGH (12410942)", bold=True, size=12, space_after=2)
    add_center(doc, "SAMEER THAKUR (12410194)", bold=True, size=12, space_after=12)

    add_center(doc, "UNDER THE GUIDANCE OF", size=12, space_after=4)
    add_center(doc, "Prof. Dr. Nakul Sharma", size=10, space_after=16)

    add_center(doc, "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING", bold=True, size=11, space_after=2)
    add_center(doc, "INTERNET OF THINGS CYBER SECURITY INCLUDING", bold=True, size=11, space_after=0)
    add_center(doc, "BLOCKCHAIN TECHNOLOGY", bold=True, size=11, space_after=12)

    add_center(doc, "BANSILAL RAMNATH AGARWAL CHARITABLE TRUST\u2019S", size=11, space_after=2)
    add_center(doc, "VISHWAKARMA INSTITUTE OF TECHNOLOGY", bold=True, size=13, space_after=2)
    add_center(doc, "(An Autonomous Institute affiliated to Savitribai Phule Pune University)",
               size=11, space_after=8)
    add_center(doc, "2026 - 2027", bold=True, size=13, space_after=4)

    doc.add_page_break()

    # ===========================================================================
    # CERTIFICATE PAGE
    # ===========================================================================
    add_center(doc, "BANSILAL RAMNATH AGARWAL CHARITABLE TRUST\u2019S", bold=True, size=12, space_after=2)
    add_center(doc, "VISHWAKARMA INSTITUTE OF TECHNOLOGY", bold=True, size=14, space_after=2)
    add_center(doc, "(An Autonomous Institute affiliated to Savitribai Phule Pune University)",
               bold=True, size=11, space_after=2)
    add_center(doc, "PUNE \u2013 411037", size=12, space_after=16)

    add_section_title(doc, "CERTIFICATE", size=15, space_after=12)

    add_para(doc, (
        "This is to certify that the Course Project titled \u201cML-Based CPU Scheduler: "
        "Direct Policy Learning with Reinforcement Learning\u201d submitted by "
        "Sharad Shinde (12412393), Yash Wagh (12410942) and Sameer Thakur (12410194) are in "
        "partial fulfilment for the award of the Degree of Bachelor of Technology in Department of "
        "CSE-IOTCSBT of Vishwakarma Institute of Technology, Savitribai Phule Pune University. "
        "This course project report is a record of Bonafide work carried out by them under my guidance "
        "during the academic year 2026-27."
    ), size=12, space_after=24)

    add_para(doc, "Guide", bold=True, size=12, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=2)
    add_para(doc, "Prof. Dr. Nakul Sharma", size=12, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=16)
    add_para(doc, "HOD", bold=True, size=12, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=2)
    add_para(doc, "Prof. Dr. Priya Shelke", size=12, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=24)
    add_para(doc, "Place: VIT, Pune", size=12, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=2)
    add_para(doc, "Date: ", size=12, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=12)

    doc.add_page_break()

    # ===========================================================================
    # PROJECT DETAILS
    # ===========================================================================
    add_center(doc, "Bansilal Ramnath Agarwal Charitable Trust\u2019s", size=11, space_after=2)
    add_center(doc, "Vishwakarma Institute of Technology, Pune-37", bold=True, size=12, space_after=2)
    add_center(doc, "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING", bold=True, size=11, space_after=2)
    add_center(doc, "INTERNET OF THINGS CYBER SECURITY INCLUDING BLOCKCHAIN TECHNOLOGY",
               size=10, space_after=12)

    add_section_title(doc, "PROJECT DETAILS", size=15, space_after=10)

    add_para(doc, "Group No :  ", size=12, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=6)
    add_para(doc, "Members:", bold=True, size=12, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=6)

    make_table(doc,
               ["Roll No.", "PRN", "Name of Student", "Contact No.", "Email ID"],
               [
                   ["33", "12412393", "Sharad Shinde", "+917498560593", "sharad.shinde24@vit.edu"],
                   ["56", "12413834", "Yash Wagh", "+917387369263", "yash.wagh24@vit.edu"],
                   ["43", "12413280", "Sameer Thakur", "+918262926847", "sameer.thakur24@vit.edu"],
               ])

    add_empty_para(doc, 8)
    add_para(doc, "Academic Year:  2026-2027", size=12, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=4)
    add_para(doc, "Project Title:  ML-Based CPU Scheduler: Direct Policy Learning with Reinforcement Learning",
             size=12, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=4)
    add_para(doc, "Project Area:  Operating Systems, Reinforcement Learning & Machine Learning",
             size=12, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=4)
    add_para(doc, "Internal Guide:  Dr. Nakul Sharma", size=12, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=16)
    add_para(doc, "Signature of Internal Guide", size=12, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=12)

    doc.add_page_break()

    # ===========================================================================
    # ACKNOWLEDGEMENT
    # ===========================================================================
    add_section_title(doc, "ACKNOWLEDGEMENT", size=15, space_after=12)

    add_para(doc, (
        "We would like to sincerely thank our project supervisor, Prof. Dr. Nakul Sharma, for his valuable "
        "guidance, constant encouragement and the constructive suggestions he has given us during this project. "
        "Because of his support we were able to gain an understanding of the practical challenges involved in "
        "applying Reinforcement Learning to operating system scheduling problems."
    ), size=12, space_after=8)

    add_para(doc, (
        "We would like to express our gratitude to Prof. Dr. Priya Shelke, who is the Head of the Department "
        "of Computer Science & Engineering (covering the fields of Internet of Things, Cyber Security including "
        "Blockchain Technology), as well as to the faculty and staff of Vishwakarma Institute of Technology in "
        "Pune, for having made the facilities and academic environment available which were necessary for "
        "carrying out this work."
    ), size=12, space_after=8)

    add_para(doc, (
        "We should also express our thanks to our friends and our families for the support, patience and "
        "motivation they have shown us throughout the development of this project."
    ), size=12, space_after=16)

    add_para(doc, "Sharad Shinde", size=12, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=2)
    add_para(doc, "Yash Wagh", size=12, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=2)
    add_para(doc, "Sameer Thakur", size=12, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=12)

    doc.add_page_break()

    # ===========================================================================
    # ABSTRACT
    # ===========================================================================
    add_section_title(doc, "ABSTRACT", size=15, space_after=12)

    add_para(doc, (
        "CPU scheduling is a fundamental problem in operating systems that directly impacts system responsiveness, "
        "throughput and fairness. Traditional scheduling algorithms such as First-Come-First-Served (FCFS), "
        "Shortest Job First (SJF), Round Robin (RR) and Multi-Level Feedback Queue (MLFQ) rely on fixed "
        "heuristics or require prior knowledge of process burst times that is unavailable in practice. "
        "The present project introduces an ML-based CPU scheduler that uses Deep Reinforcement Learning (DRL) "
        "\u2014 specifically, a Deep Q-Network (DQN) \u2014 to learn a direct dispatch policy from observable system "
        "state, without access to true burst times."
    ), size=12, space_after=8)

    add_para(doc, (
        "The RL agent observes the top-K (K=8) candidates in the ready queue, with features including "
        "normalised waiting time, priority, CPU and memory request, and a historical average burst estimate "
        "derived from previously completed tasks of the same job. True burst time is strictly hidden from the "
        "agent, mirroring real-world kernel constraints. The agent is trained on a synthetic trace modelled "
        "after the Google Cluster Data 2011 schema and evaluated against five classical baselines (FCFS, SJF, "
        "SRTF, Round Robin, MLFQ) on a held-out, time-split test set of 150 processes."
    ), size=12, space_after=8)

    add_para(doc, (
        "Results show that the DQN agent achieves an average waiting time of 739.4 seconds, outperforming "
        "FCFS (989.4) by approximately 25%. While it does not surpass the preemptive baselines (RR: 423.8, "
        "MLFQ: 406.9) or the oracle schedulers (SJF: 171.3, SRTF: 169.7), this is an expected and "
        "explainable outcome: the agent operates non-preemptively and without future knowledge. Diagnostic "
        "ceiling analyses confirm the gap is a training-optimisation problem rather than an information "
        "limitation. The project includes a full web-based interactive showcase with step-by-step simulation, "
        "Gantt chart visualisation, benchmark comparison and a viva defence guide."
    ), size=12, space_after=8)

    add_para(doc, (
        "Keywords: CPU Scheduling, Reinforcement Learning, Deep Q-Network, Operating Systems, Process "
        "Dispatch, Markov Decision Process, Gymnasium, Stable-Baselines3, Google Cluster Trace."
    ), italic=True, size=11, space_after=12)

    doc.add_page_break()

    # ===========================================================================
    # INDEX
    # ===========================================================================
    add_section_title(doc, "INDEX", size=15, space_after=10)

    make_table(doc,
               ["Sr. No.", "Title", "Chapter"],
               [
                   ["1", "Introduction to the Project", "1"],
                   ["2", "Theory", "2"],
                   ["3", "Tools Used for the Project", "3"],
                   ["4", "Results and Discussion", "4"],
                   ["5", "Conclusion", "5"],
               ])

    doc.add_page_break()

    # ===========================================================================
    # CHAPTER 1 — INTRODUCTION
    # ===========================================================================
    add_section_title(doc, "1. Introduction to the Project", size=15, space_after=10)

    add_para(doc, (
        "CPU scheduling is the core mechanism by which an operating system decides which process from the "
        "ready queue should be dispatched to the CPU next. The choice of scheduling algorithm has a direct "
        "impact on average waiting time, turnaround time, response time and overall system throughput. "
        "Classical algorithms such as FCFS, SJF, SRTF, Round Robin and MLFQ have been studied extensively "
        "and are deployed in real operating systems. However, each has well-known limitations: FCFS suffers "
        "from the convoy effect, SJF/SRTF require knowledge of true burst times (oracle information), "
        "and Round Robin/MLFQ depend on manually tuned time quanta."
    ), size=12, space_after=8)

    add_para(doc, (
        "Machine Learning, and in particular Reinforcement Learning (RL), offers an alternative approach. "
        "Instead of encoding fixed scheduling rules, an RL agent can learn a dispatch policy directly from "
        "interaction with a simulated environment, optimising a reward signal tied to the scheduling objective "
        "(e.g., minimising average waiting time). The agent observes the state of the ready queue and picks "
        "the next process to dispatch, receiving feedback on how that decision affected the overall system."
    ), size=12, space_after=8)

    add_para(doc, (
        "This project, titled \u201cML-Based CPU Scheduler: Direct Policy Learning with Reinforcement Learning\u201d, "
        "formulates CPU scheduling as a Markov Decision Process (MDP) and trains a Deep Q-Network (DQN) agent "
        "to act as the scheduler. The agent is trained using the Stable-Baselines3 library with a Gymnasium "
        "environment that faithfully simulates non-preemptive dispatch semantics, accurate waiting-time "
        "accounting for processes arriving during a dispatch, and realistic feature constraints (true burst "
        "time is hidden from the agent)."
    ), size=12, space_after=8)

    add_para(doc, "The specific objectives are:", bold=True, size=12, space_after=4)
    objectives = [
        "To formulate CPU scheduling as an MDP with a carefully designed state space, action space, transition function and reward signal.",
        "To train a DQN agent that learns to dispatch processes using only information a real scheduler could observe (waiting time, priority, resource requests, historical burst averages).",
        "To evaluate the trained agent against five classical baselines (FCFS, SJF, SRTF, Round Robin, MLFQ) on a held-out, time-split test trace.",
        "To compute diagnostic ceiling analyses (true-burst windowed oracle, realistic proxy oracle) to understand the gap between agent performance and theoretical limits.",
        "To build an interactive web-based showcase with step-by-step simulation, Gantt charts, comparative benchmarks and a viva defence guide.",
        "To analyse the advantages and limitations of using RL for CPU scheduling and identify future improvements.",
    ]
    for obj in objectives:
        add_bullet(doc, obj)

    add_para(doc, (
        "The system uses a synthetic trace modelled after the Google Cluster Data 2011 schema, with jobs "
        "that have characteristic latent duration classes and whose tasks are interleaved over time. This "
        "ensures that a time-based train/test split preserves job history overlap, allowing the historical "
        "burst feature to generalise realistically to the test period."
    ), size=12, space_after=12)

    doc.add_page_break()

    # ===========================================================================
    # CHAPTER 2 — THEORY
    # ===========================================================================
    add_section_title(doc, "2. Theory", size=15, space_after=10)

    # 2.1
    add_subsection_title(doc, "2.1 CPU Scheduling in Operating Systems")
    add_para(doc, (
        "CPU scheduling is the problem of selecting which process from the ready queue should next be given "
        "CPU time. The scheduler must balance competing objectives: minimising average waiting time and "
        "turnaround time, maximising throughput, and ensuring fairness among processes. Classical approaches "
        "include:"
    ), size=12, space_after=6)

    make_table(doc,
               ["Algorithm", "Type", "Key Characteristic"],
               [
                   ["FCFS", "Non-preemptive", "Dispatches in arrival order; suffers convoy effect"],
                   ["SJF", "Non-preemptive (oracle)", "Picks shortest burst; optimal avg wait but requires future knowledge"],
                   ["SRTF", "Preemptive (oracle)", "Preempts for shorter remaining time; requires future knowledge"],
                   ["Round Robin", "Preemptive", "Fixed time quantum; fair but high context-switch overhead"],
                   ["MLFQ", "Preemptive", "Multiple priority queues with aging; adapts to process behaviour"],
               ])

    add_empty_para(doc, 8)

    # 2.2
    add_subsection_title(doc, "2.2 Reinforcement Learning for Sequential Decision-Making")
    add_para(doc, (
        "Reinforcement Learning (RL) is a framework for sequential decision-making where an agent interacts "
        "with an environment over discrete time steps. At each step, the agent observes the current state, "
        "selects an action according to its policy, receives a reward, and transitions to a new state. The "
        "goal is to learn a policy that maximises cumulative discounted reward. CPU scheduling maps naturally "
        "to this framework: each dispatch decision is an action, the ready queue state is the observation, "
        "and the negative waiting time accrued is the reward."
    ), size=12, space_after=8)

    # 2.3
    add_subsection_title(doc, "2.3 Deep Q-Networks (DQN)")
    add_para(doc, (
        "DQN (Mnih et al., 2015) approximates the optimal action-value function Q*(s, a) using a neural "
        "network. It employs experience replay (storing transitions in a buffer and sampling mini-batches) "
        "and a target network (a delayed copy of the Q-network) to stabilise training. For CPU scheduling, "
        "the Q-network takes the flattened ready-queue feature vector as input and outputs Q-values for each "
        "of the K candidate slots, allowing the agent to pick the slot with the highest estimated value."
    ), size=12, space_after=8)

    # 2.4
    add_subsection_title(doc, "2.4 MDP Formulation for CPU Scheduling")
    add_para(doc, "The scheduling problem is formulated as a Markov Decision Process:", bold=True, size=12,
             space_after=6)

    make_table(doc,
               ["MDP Component", "Design"],
               [
                   ["State", "Top-K (K=8) ready-queue slots \u00d7 7 features + 2 global features = 58 dimensions.\n"
                             "Per-slot: [normalised_wait, priority/11, cpu_request, mem_request, hist_avg_burst, hist_count, is_valid].\n"
                             "Global: [normalised_queue_length, normalised_time].\n"
                             "TRUE burst/remaining time is strictly EXCLUDED."],
                   ["Action", "Discrete(8) \u2014 pick one of K candidate slots.\n"
                              "Invalid slot \u2192 fallback to earliest-arrived valid candidate + penalty."],
                   ["Transition", "Non-preemptive: chosen process runs to completion.\n"
                                  "Arrivals during dispatch join the queue with correct partial waiting times."],
                   ["Reward", "R = (\u2212accrued_wait \u2212 0.1 \u2212 penalty) / 100.\n"
                              "Directly optimises avg waiting time; scaled for DQN stability."],
                   ["Train/Test Split", "By time (first 70% arrivals train, later 30% test).\n"
                                        "NOT random shuffle \u2014 mirrors real deployment to unseen future traffic."],
               ],
               col_widths=[4, 13])

    add_empty_para(doc, 8)

    # 2.5
    add_subsection_title(doc, "2.5 Historical Burst Feature and Information Design")
    add_para(doc, (
        "Since true burst time is hidden, the agent relies on a historical average burst estimate: the "
        "running mean of burst times of previously completed tasks sharing the same job_id. This mirrors "
        "how real schedulers (such as Google Borg) estimate task durations from recurring job patterns. "
        "The synthetic trace interleaves each job\u2019s tasks across the entire time range so that a time-based "
        "train/test split still provides historical data for test-period jobs \u2014 100% job overlap between "
        "train and test splits was verified."
    ), size=12, space_after=8)

    # 2.6
    add_subsection_title(doc, "2.6 Diagnostic Ceiling Analysis")
    add_para(doc, (
        "Three diagnostic baselines establish the performance landscape and separate information limitations "
        "from training limitations:"
    ), size=12, space_after=6)

    make_table(doc,
               ["Diagnostic", "Avg Wait", "Description"],
               [
                   ["True-burst windowed oracle", "424.6",
                    "Looks at the same 8 candidate slots as the agent, picks lowest TRUE burst (cheating). "
                    "Ceiling imposed by the 8-slot window."],
                   ["Realistic proxy oracle", "449.0",
                    "Same 8 slots, picks using only the historical-avg-burst feature (no cheating). "
                    "Proves the feature is highly informative."],
                   ["DQN best checkpoint", "739.4",
                    "Actual trained agent. Gap to proxy oracle = training/optimisation problem, "
                    "not information problem."],
               ],
               col_widths=[5, 2.5, 10])

    add_empty_para(doc, 8)

    # 2.7
    add_subsection_title(doc, "2.7 DQN Training Instability on Scheduling Tasks")
    add_para(doc, (
        "DQN is known to be unstable on tasks with long, variable-length episodes and delayed, variable-scale "
        "rewards \u2014 exactly what non-preemptive scheduling produces. One action can \u2018cost\u2019 anywhere from a "
        "fraction of a second to 100+ seconds of simulated time. Across many hyperparameter configurations, "
        "DQN repeatedly finds a decent policy early in training (~700\u2013800 avg wait within the first 20\u201340k "
        "steps) and then degrades with further training rather than converging. This motivated saving the "
        "best checkpoint by held-out performance rather than using the final model."
    ), size=12, space_after=8)

    # 2.8
    add_subsection_title(doc, "2.8 Evaluation Metrics")
    add_para(doc, "The following metrics are used to compare schedulers:", size=12, space_after=6)

    make_table(doc,
               ["Metric", "Formula / Definition"],
               [
                   ["Average Waiting Time", "Mean time each process spends in the ready queue before completing execution."],
                   ["Average Turnaround Time", "Mean time from arrival to completion (waiting + burst)."],
                   ["Average Response Time", "Mean time from arrival to first dispatch."],
                   ["Throughput", "Number of completed processes / makespan."],
                   ["Makespan", "Total elapsed time from first arrival to last completion."],
               ])

    doc.add_page_break()

    # ===========================================================================
    # CHAPTER 3 — TOOLS USED
    # ===========================================================================
    add_section_title(doc, "3. Tools Used for the Project", size=15, space_after=10)

    add_subsection_title(doc, "3.1 Programming Language \u2014 Python")
    add_para(doc, (
        "Python is used for all software components including the simulation environment, RL training, "
        "evaluation, trace generation and the web-based showcase. Its ecosystem of machine learning, "
        "data science and web development libraries makes it the natural choice."
    ), size=12, space_after=8)

    add_subsection_title(doc, "3.2 Gymnasium (OpenAI Gym)")
    add_para(doc, (
        "Gymnasium provides the standard API for RL environments. The custom SchedulerEnv class implements "
        "the gym.Env interface with reset(), step(), observation_space and action_space, enabling seamless "
        "integration with any RL algorithm library."
    ), size=12, space_after=8)

    add_subsection_title(doc, "3.3 Stable-Baselines3 (SB3)")
    add_para(doc, (
        "Stable-Baselines3 provides reliable implementations of RL algorithms in PyTorch. The project "
        "uses SB3\u2019s DQN implementation with an MlpPolicy (two hidden layers of 128 units each). Key "
        "hyperparameters: learning rate 1e-4, buffer size 50K, batch size 64, gamma 0.99, target update "
        "interval 1000, exploration fraction 0.3."
    ), size=12, space_after=8)

    add_subsection_title(doc, "3.4 PyTorch")
    add_para(doc, (
        "PyTorch serves as the deep learning backend for Stable-Baselines3, handling the DQN neural "
        "network forward/backward passes, experience replay sampling, and gradient updates."
    ), size=12, space_after=8)

    add_subsection_title(doc, "3.5 NumPy, Pandas and Matplotlib")
    add_para(doc, (
        "NumPy: array operations for state construction and normalisation. "
        "Pandas: loading and manipulating trace data CSVs (Google Cluster Data 2011 schema). "
        "Matplotlib: generating comparison bar charts of scheduler performance metrics."
    ), size=12, space_after=8)

    add_subsection_title(doc, "3.6 Flask and Flask-CORS")
    add_para(doc, (
        "Flask powers the web-based interactive showcase, serving a single-page application with REST API "
        "endpoints for step-by-step simulation, batch benchmarks, workload management and viva reference "
        "data. Flask-CORS enables cross-origin requests for development."
    ), size=12, space_after=8)

    add_subsection_title(doc, "3.7 Google Cluster Data 2011 Trace Schema")
    add_para(doc, (
        "The project uses the task_events schema from the Google Cluster Data 2011 dataset. The trace "
        "loader parses event types (SUBMIT, SCHEDULE, FINISH, KILL) to derive arrival times and burst "
        "durations. A synthetic trace generator produces data in the same schema, allowing all downstream "
        "code to work identically on real or synthetic data."
    ), size=12, space_after=8)

    add_subsection_title(doc, "3.8 Development Environment")
    add_para(doc, (
        "Training and evaluation were carried out locally using Python 3.13 on Windows. The web "
        "showcase runs on Flask\u2019s development server (localhost:5000)."
    ), size=12, space_after=8)

    add_subsection_title(doc, "3.9 Summary of Tools")

    make_table(doc,
               ["Tool / Library", "Purpose"],
               [
                   ["Python 3.13", "Core programming language for all components"],
                   ["Gymnasium", "Standard RL environment API (SchedulerEnv)"],
                   ["Stable-Baselines3", "DQN training, evaluation, model checkpoint management"],
                   ["PyTorch", "Deep learning backend for DQN neural network"],
                   ["NumPy", "Array operations, feature normalisation"],
                   ["Pandas", "Trace data loading and manipulation"],
                   ["Matplotlib", "Performance comparison plots"],
                   ["Flask + Flask-CORS", "Web dashboard backend and REST API"],
                   ["HTML/CSS/JavaScript", "Interactive frontend (Gantt charts, step-by-step simulator)"],
                   ["Google Cluster Data 2011 Schema", "Trace format for real and synthetic workloads"],
               ])

    doc.add_page_break()

    # ===========================================================================
    # CHAPTER 4 — RESULTS AND DISCUSSION
    # ===========================================================================
    add_section_title(doc, "4. Results and Discussion", size=15, space_after=10)

    # 4.1
    add_subsection_title(doc, "4.1 System Workflow")
    steps = [
        "Step 1: A synthetic trace (or real Google Cluster Data 2011 trace) is loaded and parsed into Process objects with arrival time, burst time, priority, CPU/memory requests and job ID.",
        "Step 2: The trace is split by time \u2014 the first 70% of arrivals form the training set (350 processes), the remaining 30% form the held-out test set (150 processes).",
        "Step 3: The SchedulerEnv Gymnasium environment is initialised with the training trace. It presents the top-8 ready-queue candidates as a 58-dimensional observation vector.",
        "Step 4: The DQN agent trains for 250,000 timesteps, with periodic evaluation on the test split every 5,000 steps. The best checkpoint by held-out average waiting time is saved.",
        "Step 5: After training, the best DQN checkpoint and all five classical baselines (FCFS, SJF, SRTF, RR, MLFQ) are evaluated on the same 150-process test trace.",
        "Step 6: Results are saved to comparison.json and a bar chart (comparison.png). The web showcase provides interactive exploration of the results.",
    ]
    for s in steps:
        add_bullet(doc, s)

    add_empty_para(doc, 6)

    # 4.2
    add_subsection_title(doc, "4.2 Scheduler Comparison Results")
    add_para(doc, (
        "All schedulers were evaluated on the same held-out test set of 150 processes (later-arriving "
        "30% of the trace). The following table presents the key metrics:"
    ), size=12, space_after=6)

    make_table(doc,
               ["Scheduler", "Avg Waiting\nTime", "Avg Turnaround\nTime", "Avg Response\nTime", "Throughput", "Completed"],
               [
                   ["FCFS", "989.4", "1005.4", "989.4", "0.0624", "150"],
                   ["RL (DQN, best)", "739.4", "755.4", "739.4", "0.0624", "150"],
                   ["Round Robin (q=2s)", "423.8", "439.8", "73.0", "0.0624", "150"],
                   ["MLFQ (3 levels)", "406.9", "422.9", "2.6", "0.0624", "150"],
                   ["SJF (oracle)", "171.3", "187.4", "171.3", "0.0624", "150"],
                   ["SRTF (oracle)", "169.7", "185.7", "168.7", "0.0624", "150"],
               ])

    add_empty_para(doc, 6)

    # Insert comparison chart
    if os.path.exists(COMPARISON_IMG):
        add_center(doc, "Figure 1: Scheduler Comparison \u2014 Average Waiting Time (held-out test set)",
                   bold=True, size=11, space_after=6)
        doc.add_picture(COMPARISON_IMG, width=Inches(5.5))
        last_paragraph = doc.paragraphs[-1]
        last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_empty_para(doc, 8)

    # 4.3
    add_subsection_title(doc, "4.3 Performance Analysis")

    add_para(doc, "RL vs FCFS (non-preemptive baseline):", bold=True, size=12, space_after=4)
    add_para(doc, (
        "The DQN agent reduces average waiting time from 989.4 (FCFS) to 739.4, a 25.3% improvement. "
        "Both operate non-preemptively and without oracle information, making this a fair comparison. "
        "The improvement comes from the agent learning to prefer processes with lower estimated burst "
        "times based on historical job data, partially approximating SJF-like behaviour from observable "
        "signals alone."
    ), size=12, space_after=8)

    add_para(doc, "RL vs Preemptive baselines (RR, MLFQ):", bold=True, size=12, space_after=4)
    add_para(doc, (
        "Round Robin (423.8) and MLFQ (406.9) outperform DQN (739.4) because they use preemption "
        "\u2014 slicing long processes into short time quanta prevents any single process from monopolising "
        "the CPU. The DQN agent runs each chosen process to completion, so a poor choice (dispatching "
        "a long process) incurs much higher queue-wide waiting. This is an inherent limitation of the "
        "non-preemptive dispatch model, not of the RL approach itself."
    ), size=12, space_after=8)

    add_para(doc, "RL vs Oracle baselines (SJF, SRTF):", bold=True, size=12, space_after=4)
    add_para(doc, (
        "SJF (171.3) and SRTF (169.7) are theoretical lower bounds that cheat by knowing each process\u2019s "
        "true burst time in advance. No real scheduler can match them. They serve as reference points "
        "to contextualise the RL agent\u2019s performance."
    ), size=12, space_after=8)

    # 4.4
    add_subsection_title(doc, "4.4 Ceiling Analysis and Information Gap")

    make_table(doc,
               ["Analysis", "Avg Waiting Time", "Significance"],
               [
                   ["FCFS (baseline)", "989.4", "No intelligence \u2014 pure arrival order."],
                   ["DQN best checkpoint", "739.4", "25% better than FCFS using only observable features."],
                   ["Realistic proxy oracle", "449.0",
                    "Optimal use of the same features the agent has. Gap to DQN = training problem."],
                   ["True-burst windowed oracle", "424.6",
                    "Optimal with true burst in 8-slot window. Close to proxy \u2192 feature is informative."],
                   ["Full SJF (oracle)", "171.3",
                    "Global oracle (all queue). Window constraint costs ~253 units."],
               ],
               col_widths=[5, 3.5, 9])

    add_empty_para(doc, 4)
    add_para(doc, (
        "The ceiling analysis demonstrates that the information available to the agent (historical burst "
        "averages) is sufficient to reach ~449.0 avg wait \u2014 close to the true-burst ceiling of 424.6. "
        "The gap between DQN\u2019s actual performance (739.4) and the proxy oracle (449.0) is therefore a "
        "training/optimisation problem, not an information or environment-design problem."
    ), size=12, space_after=8)

    # 4.5
    add_subsection_title(doc, "4.5 Test Cases")

    test_cases = [
        ("Test Case 1 \u2014 Small Uniform Workload",
         "5 processes with identical burst times (5.0s each), arriving 1 second apart.",
         "RL, FCFS and SJF produce identical results (all bursts equal, optimal order is irrelevant).",
         "Confirmed \u2014 all schedulers achieve the same avg waiting time (10.0s)."),
        ("Test Case 2 \u2014 Convoy Effect Scenario",
         "One very long process (100s burst) arrives first, followed by several short processes (1s each).",
         "FCFS exhibits high avg wait (convoy). RL should detect and prefer short processes.",
         "RL dispatches the long process first (identical to FCFS) since all processes arrive simultaneously and no historical data is available. With history, RL learns to avoid long jobs."),
        ("Test Case 3 \u2014 Mixed Priority Workload",
         "Processes with varying priorities, CPU/memory requests and burst times from the test trace.",
         "RL should use priority and resource features alongside historical burst to make dispatch decisions.",
         "Confirmed \u2014 RL produces 25% lower avg wait than FCFS on the 150-process held-out test set."),
        ("Test Case 4 \u2014 Invalid Action Handling",
         "Queue has fewer than 8 processes; agent selects an invalid slot index.",
         "Environment falls back to earliest-arrived valid process and applies a small penalty.",
         "Confirmed \u2014 simulation continues without crashing; penalty signal discourages repeated invalid actions."),
    ]

    for title, inp, expected, observed in test_cases:
        add_para(doc, title, bold=True, size=12, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=4)
        make_table(doc,
                   ["", "Description"],
                   [
                       ["Input", inp],
                       ["Expected output", expected],
                       ["Observed result", observed],
                   ],
                   col_widths=[3.5, 14])
        add_empty_para(doc, 6)

    # 4.6
    add_subsection_title(doc, "4.6 Discussion")

    discussion_points = [
        "The RL agent successfully learns to approximate SJF-like scheduling from observable signals, achieving a meaningful 25% improvement over FCFS without any oracle information.",
        "The non-preemptive dispatch model is the primary limitation. Extending the action space to include preemption decisions (dispatch vs. preempt vs. continue) could close the gap to RR and MLFQ.",
        "DQN training is inherently unstable on scheduling tasks due to variable-length episodes and high-variance rewards. The best-checkpoint strategy (evaluating on held-out data every 5000 steps) is essential to extract good performance.",
        "The historical burst feature is highly informative (proxy oracle at 449.0 vs. true-burst oracle at 424.6), confirming that the feature design is sound. The remaining gap is in training, not features.",
        "The reward scaling (dividing by 100) is critical for DQN stability. Without it, raw reward values ranged from -21 to -34,205 within a single 50-step window, destabilising Q-value estimates.",
        "The time-based train/test split correctly models real deployment. The trace design ensures job history carries over to the test period, preventing the historical feature from becoming useless at evaluation time.",
    ]
    for d in discussion_points:
        add_bullet(doc, d)

    doc.add_page_break()

    # ===========================================================================
    # CHAPTER 5 — CONCLUSION
    # ===========================================================================
    add_section_title(doc, "5. Conclusion", size=15, space_after=10)

    add_para(doc, (
        "This project demonstrates that Reinforcement Learning can be applied to CPU scheduling as a "
        "direct policy learning problem. By formulating the scheduling decision as an MDP and training "
        "a DQN agent on a realistic trace, we have shown that:"
    ), size=12, space_after=6)

    conclusions = [
        "The DQN agent achieves a 25.3% reduction in average waiting time compared to FCFS (739.4 vs 989.4), using only information a real scheduler could observe \u2014 no oracle knowledge of burst times.",
        "The MDP design is carefully motivated: hiding true burst time, using log-normalised features, scaling rewards by 100, and employing a time-based data split are all necessary engineering decisions with demonstrated impact.",
        "Diagnostic ceiling analyses (proxy oracle at 449.0, true-burst oracle at 424.6) confirm that the feature design is sound and that the remaining performance gap is a training optimisation problem, not an information limitation.",
        "DQN training instability on scheduling tasks (early good policy followed by degradation) is a real and reproducible finding, mitigated by best-checkpoint saving with periodic held-out evaluation.",
        "An interactive web-based showcase enables step-by-step simulation, Gantt chart visualisation, benchmark comparison across all six schedulers, and a viva defence guide.",
    ]
    for c in conclusions:
        add_bullet(doc, c)

    add_empty_para(doc, 8)
    add_subsection_title(doc, "Future Scope")

    future_items = [
        "Extend the action space to include preemption decisions, allowing the RL agent to compete with Round Robin and MLFQ.",
        "Try Double DQN or a learning-rate decay schedule to address the early-good-then-degrades instability pattern.",
        "Use PPO with longer rollouts and proper advantage baselines as an alternative to DQN.",
        "Add proper action masking with sb3-contrib's MaskablePPO instead of the invalid-action-penalty fallback.",
        "Replace the flat top-K vector encoding with a small attention/DeepSets layer for queue-order invariance.",
        "Train and evaluate on the real Google Cluster Data 2011 trace, where stronger natural job-to-job burst correlation may yield better results.",
        "Deploy the trained model as a Linux kernel module or userspace scheduler for real-world evaluation.",
    ]
    for f in future_items:
        add_bullet(doc, f)

    add_empty_para(doc, 8)
    add_para(doc, (
        "The project demonstrates that RL-based scheduling is a viable and promising research direction. "
        "While the current DQN agent does not outperform all classical algorithms, it establishes a "
        "rigorous methodology \u2014 realistic feature constraints, proper data splitting, diagnostic ceiling "
        "analysis, and transparent reporting of both successes and limitations \u2014 that provides a solid "
        "foundation for future improvements."
    ), size=12, space_after=12)

    # ===========================================================================
    # SAVE
    # ===========================================================================
    doc.save(OUTPUT_PATH)
    print(f"Report saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_report()

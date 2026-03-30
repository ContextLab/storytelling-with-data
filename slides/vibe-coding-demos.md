---
marp: true
theme: cdl-theme
math: katex
---

# Vibe Coding in Action: Worked Examples
## Jeremy R. Manning
### PSYC 81.09: Storytelling with Data

---

## Demo 1: Building a data visualization

<div class="note-box" data-title="The goal">

We want to explore and visualize a public dataset about **global life expectancy**. Let's build an interactive chart that shows trends over time, letting users highlight specific countries and compare regions.

</div>

---

<!-- _class: scale-90 -->

## Step 1: Describe the project

<div class="example-box" data-title="A good project description">

- **Input**: CSV file with columns for country, year, and life expectancy (e.g., from Gapminder or the World Bank)
- **Output**: An interactive line chart with one line per country, a dropdown to select/highlight countries, and a tooltip showing exact values on hover
- **Desired features**: Colorblind-friendly palette, ability to compare regions (e.g., continents), responsive layout
- **Audience**: Students exploring global health trends for a data story

</div>

---

## Step 2: Spec it out

<div class="example-box" data-title="Mini user story with acceptance criteria">

**As a** student exploring global health data,
**I want** an interactive life expectancy chart
**So that** I can compare trends across countries and identify patterns.

**Acceptance criteria:**
1. Chart loads a CSV and plots life expectancy vs. year for all countries
2. User can select/deselect countries via a dropdown or legend
3. Hovering over a line shows country name, year, and value
4. Colors are distinguishable for colorblind viewers
5. Chart renders in a Jupyter notebook or as a standalone HTML file

</div>

---

<!-- _class: scale-90 -->

## Step 3: Implement and iterate

<div class="note-box" data-title="We gave Claude Code our spec. Here's what happened...">

**First attempt** produced a static matplotlib chart with all 200+ countries overlapping -- unreadable!

**Refinement prompt:**
> "The chart is too cluttered with all countries shown at once. Switch to Plotly for interactivity, default to showing only the G7 countries, and add a dropdown to select others. Use a colorblind-friendly palette and add a legend."

**Second attempt** was much better -- interactive, clean, and readable. But the dropdown didn't filter correctly.

**Follow-up prompt:**
> "The dropdown adds countries but doesn't remove them when deselected. Fix the callback so toggling a country off hides its trace."

Third time: it worked!

</div>

---

<!-- _class: scale-90 -->

## Step 4: Verify and explain

<div class="warning-box" data-title="Walk through the generated code">

Don't just run it -- **read it** and make sure you understand every section:

- **Lines 1-5**: Imports (`pandas`, `plotly.express`) and loads the CSV into a DataFrame
- **Lines 8-12**: Filters the data to the default country list (G7) and reshapes it for plotting
- **Lines 15-20**: Creates the Plotly figure with `px.line()`, setting color, hover data, and the colorblind palette
- **Lines 23-30**: Adds the dropdown menu using `updatemenus` to toggle country visibility
- **Line 32**: Displays the figure with `fig.show()`

**Ask yourself**: What would happen if a country name in the CSV doesn't match the dropdown list? Could this break?

</div>

---

## Demo 1: Takeaways

<div class="tip-box" data-title="Lessons from Demo 1">

- **Iteration is normal** -- the first output is rarely perfect. That's expected, not a failure!
- **Be specific in refinement prompts** -- "make it better" is vague; "switch to Plotly and default to G7 countries" is actionable
- **Always verify you understand the output** -- if you can't explain what a line of code does, ask the AI to explain it before moving on
- **Test edge cases** -- what happens with missing data? Unusual country names? An empty CSV?

</div>

---

## Demo 2: Building an interactive tool

<div class="note-box" data-title="The goal">

Let's build a **study flashcard app** -- a simple web tool where you can add questions and answers, quiz yourself, and track your score. This is a bigger project, so we'll use a more structured workflow.

</div>

---

<!-- _class: scale-90 -->

## Using speckit to write the spec

<div class="example-box" data-title="Running /speckit.specify">

We described the project to speckit:
> "A web-based flashcard app. Users can create decks of cards with a question on the front and answer on the back. Quiz mode shows questions one at a time, user clicks to reveal the answer, then marks correct/incorrect. Track and display the score at the end."

Speckit produced a structured spec covering:
- **Data model**: Deck, Card (question, answer), QuizSession (score, progress)
- **UI components**: Deck list, card editor, quiz view, score summary
- **Interactions**: Add/edit/delete cards, start quiz, flip card, mark answer, view results
- **Constraints**: Runs entirely in the browser (HTML/CSS/JS), no server needed

</div>

---

<!-- _class: scale-90 -->

## The plan: task breakdown

<div class="note-box" data-title="Tasks from /speckit.tasks">

1. **Task 1**: Build the HTML structure -- deck list, card editor form, quiz view container, score display
2. **Task 2**: Implement card management -- add, edit, delete cards; store in browser localStorage
3. **Task 3**: Build quiz mode -- shuffle cards, display questions, flip-to-reveal, correct/incorrect buttons
4. **Task 4**: Add scoring -- track correct/incorrect, display running score, show summary at end
5. **Task 5**: Polish -- responsive layout, keyboard shortcuts (spacebar to flip, arrow keys to navigate)

Each task is small enough to implement and test independently.

</div>

---

## Implementation: task by task

<div class="example-box" data-title="Building incrementally">

We asked Claude Code to implement **one task at a time**. After each task:

1. **Run it** -- open the HTML file in a browser and try it out
2. **Test the feature** -- does adding a card work? Does it persist after refresh?
3. **Read the code** -- understand what was generated before moving on
4. **Then move to the next task** -- "Task 1 works. Now implement Task 2: card management with localStorage."

This incremental approach means bugs are caught early, when they're small and easy to fix.

</div>

---

<!-- _class: scale-90 -->

## Debugging!

<div class="warning-box" data-title="Something went wrong">

After Task 3, the quiz mode had a bug: **it showed the answer before the question**. The card content was visible immediately instead of hidden until the user clicked "Reveal."

**Debugging prompt:**
> "In quiz mode, the answer is visible as soon as the card appears. It should be hidden until the user clicks the Reveal button. The answer div should have `display: none` initially and toggle to `display: block` on click."

**What happened**: The AI found that the `resetCard()` function wasn't being called when advancing to the next question. It added a call to `resetCard()` in the `nextQuestion()` function.

**Key insight**: Describing the **expected behavior** vs. **actual behavior** is the most effective way to report a bug.

</div>

---

## Demo 2: Verify and explain

<div class="warning-box" data-title="Before moving on: read the generated code">

Walk through the final app with a partner and explain:

- How are flashcards **stored**? (localStorage with JSON serialization)
- How does **quiz mode** select and order cards? (Fisher-Yates shuffle)
- How does the **flip animation** work? (CSS transition on a card container, toggling a class)
- How is the **score tracked**? (Counter variables incremented by button click handlers)

If you can't explain a section, **ask the AI**: "Explain what the `shuffleDeck()` function does line by line."

</div>

---

## The debugging mindset

<div class="important-box" data-title="When something goes wrong">

1. **Describe the bug clearly** -- "The answer shows before the question" is better than "it's broken"
2. **Show the AI the error message** -- copy-paste the exact error, including the traceback
3. **Ask it to explain what went wrong *before* fixing** -- understanding the cause prevents repeat bugs
4. **Verify the fix** -- don't just trust that it worked; test the specific scenario that was broken
5. **Don't just keep prompting blindly** -- if the same bug persists after 2-3 attempts, step back and re-read the code yourself

</div>

---

## Practice: Your turn!

<div class="tip-box" data-title="Choose a mini-project">

Pick one of these (or invent your own):

1. **Unit converter** -- enter a value and convert between units (miles/km, Fahrenheit/Celsius, etc.)
2. **To-do list** -- add tasks, mark them complete, filter by status, persist in localStorage
3. **Data summary tool** -- upload a CSV and display basic statistics (mean, median, min, max, histogram)

You have 20 minutes. Use the four-step workflow!

</div>

---

## Follow the workflow

<div class="example-box" data-title="Step-by-step checklist">

- [ ] **Describe**: Write 2-3 sentences about what your project does, who it's for, and what the inputs/outputs are
- [ ] **Spec**: Write a mini user story with 3-5 acceptance criteria
- [ ] **Implement**: Give your spec to Claude Code. After the first output, identify one thing to improve and write a specific refinement prompt
- [ ] **Verify and explain**: Read the generated code. Can you explain what each section does? If not, ask the AI to explain

</div>

---

## Verify and explain: pair exercise

<div class="warning-box" data-title="Before moving on">

Find a partner and take turns:

1. **Show** your partner what your project does (run it, demonstrate the features)
2. **Explain** the key code sections -- how does the main logic work? Where is data stored? What handles user input?
3. **Ask each other questions** -- "What would happen if the user enters invalid input?" "How would you add a new feature?"

If you can explain it, you understand it. If you can't, that's your next learning opportunity.

</div>

---

<!-- _class: scale-90 -->

## When to use which approach

<div class="note-box" data-title="Matching the workflow to the task">

| Task complexity | Approach | Example |
|-|-|-|
| **Simple** (< 10 min) | One-shot prompting | "Write a function that converts Celsius to Fahrenheit" |
| **Medium** (10-60 min) | Four-step workflow (describe, spec, implement, verify) | A data visualization, a simple web tool |
| **Complex** (hours/days) | Full speckit pipeline (specify, plan, tasks, implement) | A multi-page app, a data analysis pipeline |

**Rule of thumb**: If you can describe the entire project in one sentence, one-shot is fine. If you need a paragraph, use the four-step workflow. If you need a page, use speckit.

</div>

---

## Tips from the pros

<div class="tip-box" data-title="Making vibe coding work for you">

- **Be specific** -- "Add a colorblind-friendly palette with 8 distinct colors" beats "make the colors better"
- **Iterate often** -- small prompts with frequent testing beats one giant prompt
- **Test each piece** -- don't build the whole thing and then test; test after every task
- **Read the code** -- AI-generated code is *your* code now; you're responsible for understanding it
- **Keep it simple** -- start with the minimum viable version, then add features
- **Ask AI to explain** -- "Explain this function line by line" is one of the most valuable prompts you can write

</div>

---

## Summary

<div class="definition-box" data-title="Key takeaways">

- **Vibe coding is a workflow, not a one-shot prompt** -- describe, spec, implement, verify and explain
- **Verification is the most important step** -- if you can't explain the code, you don't understand the project
- **AI handles the syntax; you handle the thinking** -- you decide *what* to build and *why*; AI helps with *how*
- **Iteration is the norm** -- professionals rarely get it right on the first try either
- **The debugging mindset is a superpower** -- clear bug reports, understanding before fixing, and systematic testing will serve you in every technical endeavor

</div>

---

# Questions? Want to chat more?

<div class="emoji-figure">
  <div class="emoji-col">
    <span class="emoji emoji-xl emoji-bg emoji-bg-navy">&#x1F4E7;</span>
    <span class="label"><a href="mailto:jeremy@dartmouth.edu">Email</a> me</span>
  </div>
  <div class="emoji-col">
    <span class="emoji emoji-xl emoji-bg emoji-bg-purple">&#x1F4AC;</span>
    <span class="label">Join our <a href="https://stories-about-data.slack.com">Slack</a></span>
  </div>
  <div class="emoji-col">
    <span class="emoji emoji-xl emoji-bg emoji-bg-green">&#x1F481;</span>
    <span class="label">Come to <a href="https://context-lab.com/scheduler">office hours</a></span>
  </div>
</div>

<div class="note-box" data-title="Up next...">

- Check the course schedule for what's coming next

</div>

# Importing dependencies from transformers
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

# Load tokenizer
tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-large")

# Load model
model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-large")


text = """
This video is part of a fourpart series on Thinking Ahead. In this video, we discuss
identifying inputs and outputs in a given situation. Thinking Ahead is an essential skill. It will
help you to maximize code efficiency and minimize errors. One of the first tasks when designing a
new system is to determine what inputs the system needs and what outputs the system should produce.
A typical approach is to start by deciding what your system needs to output. What is its goal? Most
systems are designed to produce an output of some kind, whether it be visual onscreen or printed in
a physical format, audio, some form of haptic feedback or data to be input into another process or
system. Once you understand what your system does, you can backtrack and work out the inputs it will
need to produce the desired outputs. For example, imagine a computer company that offers onsite
repairs, upgrades, and maintenance for a fixed cost per service. Here's an example of a digital
invoice. This would be an output from a company system and could be generated automatically as part
of an online ordering process. What inputs would need to go into the system in order to generate the
data required to produce this automatic invoice? Pause the video and study the invoice and see if
you can come up with a list. So hopefully you identified most of these data items on the invoice.
Each of these would need to be input into the system in some form or another to end up producing the
output in the form of the automatic PDF invoice. Now, in terms of writing a computer program, you
need to be able to identify the inputs, processes and the outputs under exam conditions. This will
usually relate to a provided scenario. So let's have a look at the easy scenario here. Write a
program to calculate the volume of a fish tank based on its dimensions and report the results to the
user. So you can see here we would require the user to input the length, height and depth of the
fish tank. Now this is assuming a sort of cubeshaped fish tank, so it's quite a simple example. We
would need to process that information times the length by the height, size and depth and the output
then would be a number, a real or float the volume of the fish tank. Okay, let's look at another
example. But this time you have a go. So we're going to write a program that asks the user for the
number of students in their class and prompts them to enter each student's test score within the
range not to 100. It should then output the highest, lowest and average score. So pause the video
and figure out what are the inputs and outputs to the system and what processes have to happen to
turn those inputs into the outputs. Okay, so we've got here that we should input the number of
students and obviously the current score will need to be input by each student. The output literally
from the scenario should be the smallest score, min score, the Max score and the average. And then
obviously there's some processing in the middle to work out those values and that's where your
algorithm or your code would go. So having watched this video you should be able to answer the
following key question. Why is it important to identify the inputs and outputs of a system and what
form can those inputs and outputs take to help get your head around everything to do with
computational thinking, we have a freely available downloadable cheat sheet. It's got two sides to
it. There's a basic poster that reminds you at the top level what the five different strands are and
on the back there's a much more detailed explanation. This resource is completely free from student
craigandave.org. Just scroll down and select the section that says a level revision. You'll then see
a section called OCR as and a level and there's a number of cheat sheets in there including two
versions of the computation. One just click download to get the zip file you.
"""

tokens = tokenizer(text, truncation=True, padding="longest", return_tensors="pt")

summary = model.generate(**tokens, min_length=200)


print(tokenizer.decode(summary[0]))
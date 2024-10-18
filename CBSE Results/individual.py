import csv

# Define the input and output file names
input_file = 'results.csv'
output_file = 'PCB.csv'

# Main subjects
main_subjects = ['PHYSICS', 'CHEMISTRY', 'BIOLOGY', 'ENGLISH CORE']

# Extra subjects
extra_subjects = [
    'ARTIFICIAL INTELLIGENCE', 'PHYSICAL EDUCATION', 'PSYCHOLOGY', 'HOME SCIENCE',
    'HISTORY', 'POLITICAL SCIENCE', 'GEOGRAPHY', 'INFORMATICS PRACTICE',
    'TOURISM', 'FOOD PRODUCTION', 'COMPUTER SCIENCE', 'ECONOMICS',
    'BUSINESS STUDIES', 'ACCOUNTANCY', 'INSURANCE', 'FRONT OFFICE OPERATIONS'
]

# Read the input file and process the data
students = []
with open(input_file, mode='r', newline='') as infile:
    reader = csv.DictReader(infile)
    
    for row in reader:
        # Check if the Mathematics field is not empty
        if row['BIOLOGY']:
            # Gather main subject marks
            main_marks = [float(row[subject]) for subject in main_subjects if row[subject]]

            # Find the highest mark among the extra subjects
            max_extra_mark = 0
            for subject in extra_subjects:
                if row[subject] and float(row[subject]) > max_extra_mark:
                    max_extra_mark = float(row[subject])

            # Calculate the new average
            if main_marks:
                total_marks = sum(main_marks) + max_extra_mark
                percentage = total_marks / (len(main_marks) + 1)
            else:
                percentage = 0

            # Prepare the student data
            student_data = {
                'S. No.': len(students) + 1,
                'NAME': row['NAME'],
                'PERCENTAGE': percentage,
                'PHYSICS': row['PHYSICS'],
                'CHEMISTRY': row['CHEMISTRY'],
                'BIOLOGY': row['BIOLOGY'],
                'ENGLISH': row['ENGLISH CORE'],
                'AI': row['ARTIFICIAL INTELLIGENCE'],
                'PE': row['PHYSICAL EDUCATION'],
                'PSYCHOLOGY': row['PSYCHOLOGY'],
                'HOME SCIENCE': row['HOME SCIENCE'],
                'INFORMATICS PRACTICE': row['INFORMATICS PRACTICE']
            }
            
            # Add the student data to the list
            students.append(student_data)

# Sort the students by average in descending order
students_sorted = sorted(students, key=lambda x: x['PERCENTAGE'], reverse=True)

# Write the sorted data to the output CSV file
with open(output_file, mode='w', newline='') as outfile:
    fieldnames = ['S. No.', 'NAME', 'PERCENTAGE', 'PHYSICS', 'CHEMISTRY', 'BIOLOGY', 'ENGLISH', 'AI', 'PE', 'PSYCHOLOGY', 'HOME SCIENCE', 'INFORMATICS PRACTICE']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    
    # Write the sorted student data to the CSV
    for idx, student in enumerate(students_sorted, start=1):
        student['S. No.'] = idx  # Update the serial number
        writer.writerow(student)

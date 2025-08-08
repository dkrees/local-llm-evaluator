def parse_input_data(filename):
  """Parse different file formats: Q&A pairs, Q-only, or plain text."""
  qa_pairs = []

  with open(filename, "r") as f:
      content = f.read().strip()

  filename_lower = filename.lower()

  if 'summarise_' in filename_lower :
      qa_pairs.append({"question": content, "answer": None})
  elif 'questions_' in filename_lower:
        # Handle Q&A or Q-only format
      blocks = content.split('\n\n')

      for block in blocks:
          lines = block.strip().split('\n')

          if len(lines) >= 2:
              question_line = lines[0]
              answer_line = lines[1]

              # Extract question and answer text
              if question_line.startswith('Q: ') and answer_line.startswith('A: '):
                  question = question_line[3:]  # Remove 'Q: '
                  answer = answer_line[3:]      # Remove 'A: '
                  qa_pairs.append({"question": question, "answer": answer})
          elif len(lines) == 1:
              question_line = lines[0]

              # Handle question-only format
              if question_line.startswith('Q: '):
                  question = question_line[3:]  # Remove 'Q: '
                  qa_pairs.append({"question": question, "answer": None})

  return qa_pairs

class BaseSource:


  def _cleanText(self, text):
    # Remove leading and trailing whitespace
    cleaned_text = text.strip()

    # Remove extra spaces and replace them with a single space
    cleaned_text = ' '.join(cleaned_text.split())

    return cleaned_text
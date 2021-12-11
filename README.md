# Books Web Scraping

Beautiful Soup Web scraping and email sender application.

<h2>1. Bussiness Problem.</h2>
<p>Collect Data from <a href='books.toscrape.com'>Books to Scrape</a> and save to csv.</p>
<ul>
  <dl>
    <dt>Book Category.</dt>
      <li>Classics.</li>
      <li>Science Fiction.</li>
      <li>Humor.</li>
      <li>Bussiness.</li>
  </dl>
  <dl>
    <dt>Book Info.</dt>
      <li>Name.</li>
      <li>Price.</li>
      <li>Evaluation.</li>
      <li>Stock.</li>
  </dl>
</ul>

<h2>2. Solution Strategy.</h2>
<p>Collect Data from books with Beautiful Soup python library, save the book name, price, category and stock quantity on pandas dataframe, convert to csv file and send for a user with email.</p>
<p>All this steps on app with easy layout for user, he just need to put her or someone email.</p>

![Test](https://user-images.githubusercontent.com/75986085/145502076-6abf2cd4-2968-41e5-a218-f124e0758cd3.png)

<ul>
  <dl>
    <dt>2.1. Data Collection.</dt>
    <p>Used Beautiful Soup library and requests for web scraping.</p>
  </dl>
    <dl>
    <dt>2.2. Data Cleaning.</dt>
      <p>In the first cycle, just cleaning all books prices with inflection library.</p>
  </dl>
    <dl>
    <dt>2.3. Final project.</dt>
      <p>Used pysimplegui for simple user interface email request for send the results of web scraping.</p>
  </dl>
</ul>


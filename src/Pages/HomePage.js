import Container from 'react-bootstrap/Container';
import Link from 'react-router-dom/Link';

function HomePage() {
  return (
    <Container>
      <h1>Page 1</h1>
      <Link to="/page2">Go to Page 2</Link>
    </Container>
  );
}

export default HomePage;
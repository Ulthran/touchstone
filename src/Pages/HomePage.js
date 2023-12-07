import Container from 'react-bootstrap/Container';
import { Link } from 'react-router-dom';

function HomePage({ user, signOut }) {
  return (
    <Container>
      <h1>Page 1</h1>
      <Link to="/page2">Go to Page 2</Link>

      <p>Hi {user}! Welcome to your Touchstone!</p>
    </Container>
  );
}

export default HomePage;
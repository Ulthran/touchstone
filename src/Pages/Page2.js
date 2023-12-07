import Container from 'react-bootstrap/Container';
import Link from 'react-router-dom/Link';

function Page2() {
  return (
    <Container>
      <h1>Page 2</h1>
      <Link to="/" variant="danger">
        Go to Page 1
      </Link>
    </Container>
  );
}

export default Page2;
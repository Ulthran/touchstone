import { Link } from 'react-router-dom';

function ErrorPage() {
  return (
    <div className='bg-gray-100 text-gray-800 font-sans min-h-screen flex flex-col'>
      <h1>Whoops! You're not supposed to be here. :/</h1>
      <Link to="/">
        Go back to safety.
      </Link>
    </div>
  );
}

export default ErrorPage;
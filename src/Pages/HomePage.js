import { Link } from 'react-router-dom';

import Journey from '../Components/Journey';

function HomePage({ user, signOut }) {
  return (
    <div className='container flex flex-wrap flex-col mx-auto md:w-1/2 p-4 m-4 justify-center items-center'>
      <h1>HOME PAGE</h1>
      <Link to="/page2">Go to Page 2</Link>

      <Journey />
    </div>
  );
}

export default HomePage;
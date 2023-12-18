import ReactModal from "react-modal";
import { updateJournalEntry } from '../graphql/mutations';
import { getJournalEntry } from "../graphql/queries";
import { useEffect, useState } from "react";
import HomePage from "../Pages/HomePage";

function Node({ id, client }) {
  // We can assume that a node will always exist in the db when accessed here
  const [nodeInfo, setNodeInfo] = useState({ data: { getJournalEntry: { date: "" } } });
  const [text, setText] = useState('');
  const [modalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    const fetchNodeInfo = async () => {
      const nodeInfo = await client.graphql({
        query: getJournalEntry,
        variables: {
          id: id
        }
      });

      setNodeInfo(nodeInfo);
      setText(nodeInfo.data.getJournalEntry.entry);
      console.log(nodeInfo);
    }

    fetchNodeInfo();
  }, []);

  const handleTextChange = (event) => {
    setText(event.target.value);
    console.log(text)
  };

  useEffect(() => {
    const close = (e) => {
      if (e.key === 'Escape') {
        setModalOpen(false)
      }
    }
    window.addEventListener('keydown', close)
  }, [])

  return (
    <div className="h-15 w-15 rounded-full bg-slate-500 py-4">
      <button onClick={() => { setModalOpen(true) }}>{nodeInfo.data.getJournalEntry.date}</button>
      <ReactModal
        isOpen={modalOpen}
      >
        <div className="container flex flex-wrap flex-col mx-auto md:w-1/2 p-4 m-4 justify-center items-center bg-green-100">
          <h1>Entry Page</h1>
          <h2>{nodeInfo.data.getJournalEntry.prompt}</h2>
          <textarea
            className="w-full h-96 p-4"
            placeholder="Write your entry here..."
            onChange={handleTextChange}
            value={text}>
          </textarea>
          <button className="bg-green-500" onClick={async () => {
            const updatedNodeInfo = await client.graphql({
              query: updateJournalEntry,
              variables: {
                input: {
                  id: id,
                  entry: text
                }
              }
            });

            //setNodeInfo(updatedNodeInfo);
            console.log(updatedNodeInfo);
          }}>Submit</button>
          <button className="bg-red-500" onClick={() => { setModalOpen(false) }}>Close</button>
        </div>
      </ReactModal>
    </div>
  );
}

export default Node;
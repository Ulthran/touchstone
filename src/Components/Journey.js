import Node from './Node';

import { generateClient } from 'aws-amplify/api';
import { listJournalEntries } from '../graphql/queries';
import { useEffect, useState } from 'react';

function Journey() {
    const client = generateClient();
    const [nodes, setNodes] = useState([]);
    const [nodeList, setNodeList] = useState([]);

    useEffect(() => {
        const fetchNodes = async () => {
            const nodes = await client.graphql({
                query: listJournalEntries,
                variables: {
                    limit: 100
                }
            });
            setNodes(nodes);

            const nodeList = nodes.data.listJournalEntries.items.map((node) =>
                <Node id={node.id} client={client} key={node.id} />
            );
            setNodeList(nodeList);
        }

        fetchNodes();
    }, []);

    /*const nodeList = [<Node id="12-09" client={client} />];
    console.log(nodeList);*/

    if (nodeList.length === 0) {
        nodeList.push(<div className="h-15 w-15 rounded-full bg-slate-500 py-4">No entries yet!</div>);
    }

    return (
        <div className='flex flex-col items-center overflow-y-auto w-full'>
            {nodeList}
        </div>
    )
}

export default Journey;
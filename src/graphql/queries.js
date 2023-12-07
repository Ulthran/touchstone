/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const getJournalEntry = /* GraphQL */ `
  query GetJournalEntry($id: ID!) {
    getJournalEntry(id: $id) {
      id
      date
      prompt
      entry
      createdAt
      updatedAt
      __typename
    }
  }
`;
export const listJournalEntries = /* GraphQL */ `
  query ListJournalEntries(
    $filter: ModelJournalEntryFilterInput
    $limit: Int
    $nextToken: String
  ) {
    listJournalEntries(filter: $filter, limit: $limit, nextToken: $nextToken) {
      items {
        id
        date
        prompt
        entry
        createdAt
        updatedAt
        __typename
      }
      nextToken
      __typename
    }
  }
`;

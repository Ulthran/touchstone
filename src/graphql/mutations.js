/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const createJournalEntry = /* GraphQL */ `
  mutation CreateJournalEntry(
    $input: CreateJournalEntryInput!
    $condition: ModelJournalEntryConditionInput
  ) {
    createJournalEntry(input: $input, condition: $condition) {
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
export const updateJournalEntry = /* GraphQL */ `
  mutation UpdateJournalEntry(
    $input: UpdateJournalEntryInput!
    $condition: ModelJournalEntryConditionInput
  ) {
    updateJournalEntry(input: $input, condition: $condition) {
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
export const deleteJournalEntry = /* GraphQL */ `
  mutation DeleteJournalEntry(
    $input: DeleteJournalEntryInput!
    $condition: ModelJournalEntryConditionInput
  ) {
    deleteJournalEntry(input: $input, condition: $condition) {
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

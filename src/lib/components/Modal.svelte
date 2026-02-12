<script>
  import Dialog, { Title, Content, Actions } from '@smui/dialog';
  import Button, { Label } from '@smui/button';
  
  let open = false;
</script>

<Button on:click={() => (open = true)} variant="outlined">
  <Label>View Credits</Label>
</Button>

<Dialog bind:open>
  <Title>Song Credits</Title>
  <Content>
    Written by: Freddie Mercury<br>
    Produced by: Roy Thomas Baker
  </Content>
  <Actions>
    <Button on:click={() => (open = false)}>
      <Label>Close</Label>
    </Button>
  </Actions>
</Dialog>

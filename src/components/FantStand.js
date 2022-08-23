import React from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Container, Grid} from '@material-ui/core';
import { makeStyles, withStyles } from '@material-ui/core/styles';


const StyledTableCell = withStyles((theme) => ({
    head: {
      backgroundColor: theme.palette.common.black,
      color: theme.palette.common.white,
      //may need to use media queries? idk, the table isn't rendering correctly on mobile.
      fontSize: 16,
      fontWeight: "bold"
    },
    body: {
      fontSize: 14,
    },
}))(TableCell);
  
const StyledTableRow = withStyles((theme) => ({
    root: {
      '&:nth-of-type(odd)': {
        backgroundColor: theme.palette.action.hover,
      },
    },
}))(TableRow);

const useStyles = makeStyles({
    table: {
        //got rid of this
    },
});

//so i have to use this way of creating the component
function FantStand(props) {
    
    const { standings } = props;
    const classes = useStyles();

    return standings.length !== 0 && (
      <Container>
          <Grid container direction="column" justify-content="space-evenly" alignItems="center">
              <Grid item>
              <h1>Fantasy Standings</h1>
              </Grid>
    <Grid item>
    <TableContainer component={Paper}>
      <Table className={classes.table} aria-label="customized table">
        <TableHead>
          <StyledTableRow>
            <StyledTableCell>Team</StyledTableCell>
            <StyledTableCell align="right">W</StyledTableCell>
            <StyledTableCell align="right">L</StyledTableCell>
            <StyledTableCell align="right">Win %</StyledTableCell>
          </StyledTableRow>
        </TableHead>
        <TableBody>
        {standings.map((row) => (
            <StyledTableRow key={row.name}>
              <StyledTableCell component="th" scope="row">
                {row.name}
              </StyledTableCell>
              <StyledTableCell align="right">{row.wins}</StyledTableCell>
              <StyledTableCell align="right">{row.losses}</StyledTableCell>
              <StyledTableCell align="right">{row.win_frac}</StyledTableCell>
            </StyledTableRow>
          ))}
        </TableBody>
        </Table>
        </TableContainer>
        
        </Grid>
        </Grid>
        </Container>
    );
}

export default FantStand;
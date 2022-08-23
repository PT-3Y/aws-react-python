import React from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Container, Grid } from '@material-ui/core';
import {  withStyles } from '@material-ui/core/styles';
//import { NavLink } from "react-router-dom";
import '../App.css';


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


function FantTeams(props) {

    const { teamInfo } = props;

    return teamInfo && (
       <Container>
            <Grid container direction="column" justify-content="space-evenly" alignItems="center">
{/*               <Grid item>
                    <h1>Teams</h1>
            <List>
                {teamInfo.map ((team) => (
                  <a className="stubbornLink" href={`/fantasyteams#${team.name}`}>
                    <ListItem button key={`${team.name}`}>
                      <ListItemText primary={`${team.name}`} /> 
                    </ListItem>
                  </a>
                ))}
            </List>
              </Grid> */}
            <Grid item>
            {teamInfo.map((team) => (
                <Grid item>
                    <h2 id={`${team.name}`}>{team.name}</h2>
                <TableContainer component={Paper}>
                <Table aria-label="customized table">
                  <TableHead>
                    <StyledTableRow>
                      <StyledTableCell>Team</StyledTableCell>
                      <StyledTableCell align="right">W</StyledTableCell>
                      <StyledTableCell align="right">L</StyledTableCell>
                      <StyledTableCell align="right">Win %</StyledTableCell>
                    </StyledTableRow>
                  </TableHead>
                  <TableBody>
                  {team.teams.map((mlbteam) => (
                      <StyledTableRow key={mlbteam.name}>
                      <StyledTableCell component="th" scope="row">
                        {mlbteam.name}
                      </StyledTableCell>
                      <StyledTableCell align="right">{mlbteam.wins}</StyledTableCell>
                      <StyledTableCell align="right">{mlbteam.losses}</StyledTableCell>
                      <StyledTableCell align="right">{mlbteam.win_frac}</StyledTableCell>
                    </StyledTableRow>
                  ))}
                    </TableBody>
                </Table>
                </TableContainer>
                </Grid>
            ))}   
            </Grid>                
            </Grid>
        </Container>
    );

    
}

export default FantTeams;
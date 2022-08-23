import React from 'react';
import { Container, Grid } from '@material-ui/core';

class Home extends React.Component {
    render() {
        return (
            <Container>
                <Grid className="main" container direction="column" justify-content="space-evenly" alignItems="center">
                    <Grid item>
                        <h1>Welcome to the COVID-19 MLB Fantasy League Website!</h1>
                    </Grid>
                    <Grid item>
                        <h3>
                            Big thanks to Luke for getting the league togther. I personally have not tried to figure
                            out the standings until I made this website, and I'm guessing no one else has either.
                        </h3>
                        <h3>
                            This is also the first website I've (Mike) ever made, so if you have feedback/suggestions for features
                            to add, just text me and I'll see if I can make them happen.
                        </h3>

                    </Grid>
                </Grid>
            </Container>
        );
    }
}

export default Home;
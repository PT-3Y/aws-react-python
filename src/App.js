import React from 'react';
import { Switch, Route, Redirect } from "react-router-dom";
import Layout from "./components/Layout";
import FantStand from "./components/FantStand";
import FantTeams from "./components/FantTeams";
import Home from "./components/Home";
import MLBStand from "./components/MLBStand";
import './App.css';

const API_ENDPOINT = "https://mrpuwx9zwf.execute-api.us-east-2.amazonaws.com/dev1";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      curr_standings: [],
      mlb_standings: [],
      team_info: []
    }
  }

  async get_todays_standings() {
    var response = await fetch(API_ENDPOINT + "/getfantasystandings");
    if (response.ok) {
      var json = await response.json();
      var body = JSON.parse(json.body);
      console.log(body);
      this.setState({curr_standings: body});
    } else {
      alert("HTTP-Error: " + response.status);
    }
  }

  async get_team_info() {
    var response = await fetch(API_ENDPOINT + "/getteaminfo");

    if (response.ok) {
      var json = await response.json();
      var body = JSON.parse(json.body);
      console.log(body);
      this.setState({team_info: body});
    } else {
      alert("HTTP-Error: " + response.status);
    }
  }

  async get_mlb_standings() {
    var response = await fetch(API_ENDPOINT + "/getmlbstandings");

    if (response.ok) {
      var json = await response.json();
      //var standings = JSON.parse(json);
      //console.log(standings);
      var body = JSON.parse(json.body);
      console.log(body);
      this.setState({mlb_standings: body});
    } else {
      alert("HTTP-Error: " + response.status);
    }
  }

  componentDidMount() {
    //this is where we do the API call. it runs after the page initially loads
    // this is also a good place to set the state (we do it inside this function)
    this.get_todays_standings();
    this.get_team_info();
    this.get_mlb_standings();
  }

  render() { 
    return ( 
      <Layout>
        <Switch>
          <Route exact path="/fantasystandings">
            <FantStand standings={this.state.curr_standings}/>
          </Route>
          <Route exact path = "/mlbstandings">
            <MLBStand standings={this.state.mlb_standings}/>
          </Route>
          <Route exact path="/fantasyteams">
            <FantTeams teamInfo={this.state.team_info}/>
          </Route> 
          <Route exact path="/">
            <Home />
          </Route>
          <Redirect from="*" to="/" />
        </Switch> 
      </Layout>
    );
  }
}

export default App;

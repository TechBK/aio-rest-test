/**
 * Created by quang_000 on 18/03/2016.
 */

import React from 'react'
import { Route, IndexRoute } from 'react-router'
import Layout from '../pages/Layout'
import SignInPage from '../pages/SignInPage'
import LogInPage from '../pages/LogInPage'
import Home from '../pages/Home'

const routes = (
  <Route path="/" component={Layout}>
    <IndexRoute component={Home}/>
    <Route path="signin/" component={SignInPage} />
    <Route path="login/" component={LogInPage} />
  </Route>
)

export default routes
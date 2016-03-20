/**
 * Created by techbk on 19/03/2016.
 */

import React, { Component, ProTypes } from 'react'
import { connect } from 'react-redux'
import { push } from 'react-router-redux'
import SignInForm from '../components/SignInForm'


class SignInPage extends Component {
	render(){
		return (
			<div>
				<h1>SignIn Page!!!</h1>
				<div>
					<SignInForm/>
				</div>
			</div>
		)
	}
}

export default SignInPage

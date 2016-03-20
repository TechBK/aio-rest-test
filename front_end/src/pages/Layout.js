/**
 * Created by techbk on 18/03/2016.
 */

import React, { Component, ProTypes } from 'react'
import { connect } from 'react-redux'
import { Link } from 'react-router'

class Layout extends Component {
	render(){
		return (
			<div>
				<h1>Layout</h1>
				<div>
					<ul>
						<li><Link to="/">Home</Link></li>
						<li><Link to="/signin/">Sign In</Link></li>
						<li><Link to="/login/">Log In</Link></li>
					</ul>
				</div>
				<div>{this.props.children}</div>
			</div>
		)
	}
}

export default Layout

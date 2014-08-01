/** @jsx React.DOM */
var TableRow = React.createClass({
    render: function () {
        var token = this.props.token;
        return (
            <tr>
                <td>{token.id}</td>
                <td>{token.login}</td>
                <td>{token.email}</td>
                <td>{token.value}</td>
            </tr>
            );
    }
});
var TableBody = React.createClass({
    render: function () {
        var rows = [];
        this.props.data.forEach(function (token) {
            rows.push(<TableRow token={token} />);
        });
        return (<tbody>{rows}</tbody>);
    }
});
var Table = React.createClass({
    getInitialState: function () {
        return {data: []};
    },
    componentDidMount: function () {
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            success: function (data) {
                this.setState({data: data});
            }.bind(this),
            error: function (xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    render: function () {
        return (
            <div className="col-md-9">
                <table className="table table-stripped table-bordered">
                    <thead>
                        <tr>
                            <td>ID</td>
                            <td>Login</td>
                            <td>Email</td>
                            <td>Token</td>
                        </tr>
                    </thead>
                    <TableBody data={this.state.data} />
                </table>
            </div>
            );
    }
});

var MainRow = React.createClass({
    render: function () {
        return (
            <div className="row">
                <Table url="/ajax/tokens" />
            </div>
            );
    }
});

React.renderComponent(<MainRow />, document.getElementById('main_container'));
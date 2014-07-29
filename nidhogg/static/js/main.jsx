/** @jsx React.DOM */
var TableIndex = React.createClass({
    render: function () {
        return (
            <tr>
                <td>ID</td>
                <td>Login</td>
                <td>Email</td>
                <td>Token</td>
            </tr>
            );
    }
});
var TableBody = React.createClass({
    render: function () {
        return (
            <tbody>

            </tbody>
            );
    }
});
var Table = React.createClass({
    render: function () {
        return (
            <div className="col-md-9">
                <table className="table table-stripped table-bordered">
                    <thead><TableIndex /></thead>
                    <TableBody />
                    <tfoot><TableIndex /></tfoot>
                </table>
            </div>
            );
    }
});

var MainRow = React.createClass({
    render: function () {
        return (
            <div className="row">
                <Table />
            </div>
            );
    }
});

React.renderComponent(<MainRow />, document.getElementById('main_container'));
import React, { useEffect, useState } from 'react';
import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  CircularProgress,
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  TextField,
  TablePagination
} from '@mui/material';
import { getGuests, addGuest, Guest, deleteGuest, updateGuest } from '../services/api';

const GuestManagement: React.FC = () => {
  const [guests, setGuests] = useState<Guest[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [open, setOpen] = useState(false);
  const [newGuest, setNewGuest] = useState<Partial<Guest>>({});
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(8);
  const [searchQuery, setSearchQuery] = useState('');
  const [editOpen, setEditOpen] = useState(false);
  const [currentGuest, setCurrentGuest] = useState<Partial<Guest>>({});

  useEffect(() => {
    const fetchGuests = async () => {
      try {
        const data = await getGuests();
        setGuests(data);
      } catch (err: any) {
        setError(err.message || '获取嘉宾列表失败');
      } finally {
        setLoading(false);
      }
    };

    fetchGuests();
  }, []);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setNewGuest({
      ...newGuest,
      [e.target.name]: e.target.value,
    });
  };

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(e.target.value);
  };

  const generateRandomString = () => Math.random().toString(36).substring(2, 15);

  const handleAddGuest = async () => {
    const guestToAdd = {
      name: newGuest.name || generateRandomString(),
      contact: newGuest.contact || generateRandomString(),
      email: newGuest.email,
      organization: newGuest.organization || generateRandomString(),
      location: newGuest.location || generateRandomString(),
      guest_level: typeof newGuest.guest_level === 'number' ? newGuest.guest_level : parseInt(generateRandomString(), 10),
      nationality: newGuest.nationality || generateRandomString(),
      passport: newGuest.passport || generateRandomString(),
    };

    if (!guestToAdd.email) {
      setError('电子邮箱为必填项');
      return;
    }

    try {
      const addedGuest = await addGuest(guestToAdd);
      setGuests([...guests, addedGuest]);
      handleClose();
    } catch (err: any) {
      setError(err.message || '添加嘉宾失败');
    }
  };

  const handleDeleteGuest = async (id: number) => {
    try {
      await deleteGuest(id);
      setGuests(guests.filter(guest => guest.id !== id));
    } catch (err: any) {
      setError(err.message || '删除嘉宾失败');
    }
  };

  const handleEditClickOpen = (guest: Guest) => {
    setCurrentGuest(guest);
    setEditOpen(true);
  };

  const handleEditClose = () => {
    setEditOpen(false);
  };

  const handleEditChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCurrentGuest({
      ...currentGuest,
      [e.target.name]: e.target.value,
    });
  };

  const handleUpdateGuest = async () => {
    try {
      const updatedGuest = await updateGuest(currentGuest.id!, currentGuest);
      setGuests(guests.map(guest => (guest.id === updatedGuest.id ? updatedGuest : guest)));
      handleEditClose();
    } catch (err: any) {
      setError(err.message || '更新嘉宾失败');
    }
  };

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const filteredGuests = guests.filter(guest =>
    guest.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" m={3}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Typography color="error" m={3}>
        {error}
      </Typography>
    );
  }

  return (
    <>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Button variant="contained" color="primary" onClick={handleClickOpen}>
          添加嘉宾
        </Button>
        <TextField
          size='small'
          label="搜索嘉宾"
          variant="outlined"
          value={searchQuery}
          onChange={handleSearchChange}
        />
      </Box>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>添加嘉宾</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            name="name"
            label="姓名"
            type="text"
            fullWidth
            onChange={handleChange}
          />
          <TextField
            margin="dense"
            name="contact"
            label="联系电话"
            type="text"
            fullWidth
            onChange={handleChange}
          />
          <TextField
            margin="dense"
            name="email"
            label="电子邮箱"
            type="email"
            fullWidth
            required
            onChange={handleChange}
          />
          <TextField
            margin="dense"
            name="organization"
            label="组织"
            type="text"
            fullWidth
            onChange={handleChange}
          />
          <TextField
            margin="dense"
            name="location"
            label="所在地"
            type="text"
            fullWidth
            onChange={handleChange}
          />
          <TextField
            margin="dense"
            name="guest_level"
            label="嘉宾等级"
            type="text"
            fullWidth
            onChange={handleChange}
          />
          <TextField
            margin="dense"
            name="nationality"
            label="国籍"
            type="text"
            fullWidth
            onChange={handleChange}
          />
          <TextField
            margin="dense"
            name="passport"
            label="护照"
            type="text"
            fullWidth
            onChange={handleChange}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary">
            取消
          </Button>
          <Button onClick={handleAddGuest} color="primary">
            确认
          </Button>
        </DialogActions>
      </Dialog>
      <Dialog open={editOpen} onClose={handleEditClose}>
        <DialogTitle>编辑嘉宾</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            name="name"
            label="姓名"
            type="text"
            fullWidth
            value={currentGuest.name || ''}
            onChange={handleEditChange}
          />
          <TextField
            margin="dense"
            name="contact"
            label="联系电话"
            type="text"
            fullWidth
            value={currentGuest.contact || ''}
            onChange={handleEditChange}
          />
          <TextField
            margin="dense"
            name="email"
            label="电子邮箱"
            type="email"
            fullWidth
            required
            value={currentGuest.email || ''}
            onChange={handleEditChange}
          />
          <TextField
            margin="dense"
            name="organization"
            label="组织"
            type="text"
            fullWidth
            value={currentGuest.organization || ''}
            onChange={handleEditChange}
          />
          <TextField
            margin="dense"
            name="location"
            label="所在地"
            type="text"
            fullWidth
            value={currentGuest.location || ''}
            onChange={handleEditChange}
          />
          <TextField
            margin="dense"
            name="guest_level"
            label="嘉宾等级"
            type="text"
            fullWidth
            value={currentGuest.guest_level || ''}
            onChange={handleEditChange}
          />
          <TextField
            margin="dense"
            name="nationality"
            label="国籍"
            type="text"
            fullWidth
            value={currentGuest.nationality || ''}
            onChange={handleEditChange}
          />
          <TextField
            margin="dense"
            name="passport"
            label="护照"
            type="text"
            fullWidth
            value={currentGuest.passport || ''}
            onChange={handleEditChange}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleEditClose} color="primary">
            取消
          </Button>
          <Button onClick={handleUpdateGuest} color="primary">
            确认
          </Button>
        </DialogActions>
      </Dialog>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>姓名</TableCell>
              <TableCell>联系电话</TableCell>
              <TableCell>电子邮箱</TableCell>
              <TableCell>组织</TableCell>
              <TableCell>所在地</TableCell>
              <TableCell style={{ minWidth: 120 }}>嘉宾等级</TableCell>
              <TableCell>国籍</TableCell>
              <TableCell>护照</TableCell>
              <TableCell style={{ position: 'sticky', right: 0, background: '#fff' }}>操作</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredGuests.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((guest) => (
              <TableRow key={guest.id}>
                <TableCell>{guest.id}</TableCell>
                <TableCell>{guest.name}</TableCell>
                <TableCell>{guest.contact}</TableCell>
                <TableCell>{guest.email}</TableCell>
                <TableCell>{guest.organization}</TableCell>
                <TableCell>{guest.location}</TableCell>
                <TableCell style={{ minWidth: 120 }}>{guest.guest_level}</TableCell>
                <TableCell>{guest.nationality}</TableCell>
                <TableCell>{guest.passport}</TableCell>
                <TableCell style={{ position: 'sticky', right: 0, background: '#fff' }}>
                  <Box display="flex" gap={1}>
                    <Button variant="contained" color="primary" onClick={() => handleEditClickOpen(guest)}>
                      编辑
                    </Button>
                    <Button variant="contained" color="secondary" onClick={() => handleDeleteGuest(guest.id)}>
                      删除
                    </Button>
                  </Box>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <TablePagination
          rowsPerPageOptions={[8, 10, 25]}
          component="div"
          count={filteredGuests.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </TableContainer>
    </>
  );
};

export default GuestManagement;

import React, { useState } from 'react';
import { 
  Box,
  Tabs,
  Tab,
  Typography,
  Container,
  AppBar,
  Toolbar,
  Button,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import GuestManagement from './GuestManagement';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

const Dashboard: React.FC = () => {
  const [value, setValue] = useState(0);
  const navigate = useNavigate();

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            嘉宾管理系统
          </Typography>
          <Button color="inherit" onClick={handleLogout}>
            退出登录
          </Button>
        </Toolbar>
      </AppBar>
      <Box sx={{ width: '100%' }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={value} onChange={handleChange} centered>
            <Tab label="嘉宾管理" />
            <Tab label="工作人员管理" />
            <Tab label="组委会管理" />
            <Tab label="活动管理" />
          </Tabs>
        </Box>
        <Container maxWidth="lg">
          <TabPanel value={value} index={0}>
            <GuestManagement />
          </TabPanel>
          <TabPanel value={value} index={1}>
            工作人员管理内容
          </TabPanel>
          <TabPanel value={value} index={2}>
            组委会管理内容
          </TabPanel>
          <TabPanel value={value} index={3}>
            活动管理内容
          </TabPanel>
        </Container>
      </Box>
    </Box>
  );
};

export default Dashboard;
